'''
tind.py: code for interacting with a TIND server

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from   collections import namedtuple
from   commonpy.interrupt import wait
from   commonpy.network_utils import net
from   commonpy.exceptions import NoContent, ServiceFailure, RateLimitExceeded
import json as jsonlib
from   lxml import etree, html

if __debug__:
    from sidetrack import log

from .exceptions import *
from .thumbnail_utils import thumbnail_from_google, thumbnail_from_amazon
from .record import Record


# Constants.
# .............................................................................

# Field names for finding different elements in a MARC XML record.
ELEM_RECORD       = '{http://www.loc.gov/MARC21/slim}record'
ELEM_CONTROLFIELD = '{http://www.loc.gov/MARC21/slim}controlfield'
ELEM_DATAFIELD    = '{http://www.loc.gov/MARC21/slim}datafield'
ELEM_SUBFIELD     = '{http://www.loc.gov/MARC21/slim}subfield'

# URL templates for retrieving data from a TIND server.
# The first placeholder is for the host URL; the second is for an identifier.
# Use Python .format() to substitute the relevant values into the string.
_XML_USING_BARCODE = '{}/search?p=barcode%3A+{}&of=xm'
_XML_USING_TIND_ID = '{}/search?recid={}&of=xm'

# Time in seconds we pause if we hit the rate limit, and number of times we
# repeatedly wait before we give up entirely.
_RATE_LIMIT_SLEEP = 15
_MAX_SLEEP_CYCLES = 8


# Class definitions.
# .............................................................................

class Tind():
    '''Interface to a TIND.io server.'''

    def __init__(self, server_url):
        self.server_url = server_url


    def record(self, barcode = None, tind_id = None, marc_xml = None):
        '''Return a Record object from TIND constructed from MARC XML data.

        Keword arguments "barcode", "tind_id" and "marc_xml" are mutually
        exclusive.

        If either "barcode" or "tind_id" is given, this will contact the TIND
        server, look up the record using either the barcode or the TIND id
        (depending on which one was given), download the MARC XML form of the
        TIND item data, and create the record based on data found.

        If "marc_xml" is given instead, this will create the record using
        the given XML string.  The XML must have been obtained using the MARC
        XML export feature of TIND.  Using "marc_xml" will not result in the
        TIND server being contacted.
        '''
        args = locals().copy()
        del args['self']
        given_keywords = list(keyword for keyword in args if args[keyword])
        if len(given_keywords) == 1:
            given = given_keywords[0]
            return self._record_from_argument[given](self, args[given])
        elif len(given_keywords) == 0:
            raise ValueError(f"At least one argument required, but none given")
        else:                           # More than one keyword arg given.
            given = ', '.join(given)
            raise ValueError(f"Conflicting arguments given: {given}")


    def _record_from_xml(self, xml):
        '''Initialize this record given MARC XML as a string.'''

        record = Record()
        record.tind_server = self.server_url
        # Save the XML internally in case it's useful.
        record._xml = xml

        # Parse the XML.
        if __debug__: log(f'parsing MARC XML {len(xml)} chars long')
        try:
            tree = etree.fromstring(xml, parser = etree.XMLParser(recover = True))
        except Exception as ex:
            raise ValueError(f'Bad XML')
        if len(tree) == 0:             # Blank record.
            if __debug__: log(f'blank record -- no values parsed')
            return record
        elements = tree.find(ELEM_RECORD)
        subtitle = None
        for element in elements.findall(ELEM_CONTROLFIELD):
            if element.attrib['tag'] == '001':
                record.tind_id = element.text.strip()
            elif element.attrib['tag'] == '008':
                record.year = element.text[7:11].strip()
                if not record.year.isdigit():
                    record.year = ''
        for element in elements.findall(ELEM_DATAFIELD):
            if element.attrib['tag'] == '250':
                record.edition = element.find(ELEM_SUBFIELD).text.strip()
            elif element.attrib['tag'] == '050':
                record.call_no = ''
                for subfield in element.findall(ELEM_SUBFIELD):
                    record.call_no += subfield.text.strip() + ' '
            elif element.attrib['tag'] == '090':
                # If the record has call numbers in both 050 and 090, the 090
                # value will overwrite the 050 one, and that's what we want.
                record.call_no = ''
                for subfield in element.findall(ELEM_SUBFIELD):
                    record.call_no += subfield.text.strip() + ' '
            elif element.attrib['tag'] == '100':
                for subfield in element.findall(ELEM_SUBFIELD):
                    if subfield.attrib['code'] == 'a':
                        record.main_author = subfield.text.strip()
            elif element.attrib['tag'] == '245':
                for subfield in element.findall(ELEM_SUBFIELD):
                    if subfield.attrib['code'] == 'a':
                        text = subfield.text.strip()
                        # The title sometimes contains the author names too.
                        record.title, record.author = parsed_title_and_author(text)
                    elif subfield.attrib['code'] == 'b':
                        subtitle = subfield.text.strip()
                    elif subfield.attrib['code'] == 'c':
                        record.author = subfield.text.strip()
            elif element.attrib['tag'] == '020':
                for subfield in element.findall(ELEM_SUBFIELD):
                    # Value is sometimes of the form "1429224045 (hbk.)"
                    value = subfield.text.split()[0]
                    if value.isdigit():
                        record.isbn_list.append(value)

        # We get author from 245 because in our entries, it's frequently part
        # of the title statement. If it's not, but we got an author from 100
        # use that.  100 only lists first author, but it's better than nothing.
        if record.author:
            if record.author.startswith('by'):
                record.author = record.author[2:].strip()
            elif record.author.startswith('edited by'):
                record.author = record.author[10:].strip()
        elif record.main_author:
            record.author = record.main_author

        # Caltech's TIND database contains some things that are not reading
        # materials per se. The following is an attempt to weed those out.
        if sum([not record.author, not record.year, not record.call_no]) > 1:
            for field in ['title', 'author', 'year', 'call_no', 'edition']:
                setattr(record. field, None)
            return record

        # Some cleanup work is better left until after we obtain all values.
        record.author  = cleaned(record.author)
        record.title   = cleaned(record.title)
        record.edition = cleaned(record.edition)
        record.call_no = cleaned(record.call_no)
        if subtitle:
            # A separate subtitle is not useful for us, so merge it into title.
            if subtitle.find('/') > 0:
                subtitle = subtitle[:-1].strip()
            record.title += ': ' + subtitle

        # Get other items.
        # self._get_thumbnail()
        return record


    def _record_from_barcode(self, barcode):
        record = self._record_from_id(_XML_USING_BARCODE, barcode)
        record.barcode = str(barcode)
        return record


    def _record_from_tind_id(self, tind_id):
        return self._record_from_id(_XML_USING_TIND_ID, tind_id)


    def _record_from_id(self, endpoint_template, id, retry = 0):
        (resp, error) = net('get', endpoint_template.format(self.server_url, id))
        if not error:
            if __debug__: log(f'got result from {self.server_url} for {id}')
            return self._record_from_xml(resp.content)
        elif isinstance(error, NoContent):
            if __debug__: log(f'got empty content for {id}')
            return Record()
        elif isinstance(error, RateLimitExceeded):
            retry += 1
            if retry > _MAX_SLEEP_CYCLES:
                raise ServerError(f'Rate limit exceeded for {self.server_url}')
            else:
                if __debug__: log(f'hit rate limit; pausing {_RATE_LIMIT_SLEEP}s')
                wait(_RATE_LIMIT_SLEEP)
                return self._record_from_id(endpoint_template, id, retry = retry)
        else:
            if __debug__: log(f'got {type(error)} error for {id}')
            raise ServerError(f'Problem contacting {self.server_url}: {str(error)}')


    # Initialize the dispatcher after defining the methods themselves.
    _record_from_argument = {'barcode' : staticmethod(_record_from_barcode).__func__,
                             'tind_id' : staticmethod(_record_from_tind_id).__func__,
                             'marc_xml': staticmethod(_record_from_xml).__func__}


# Miscellaneous helpers.
# .............................................................................

def cleaned(text):
    '''Mildly clean up the given text string.'''
    if not text:
        return text
    if text and text.endswith('.'):
        text = text[:-1]
    return text.strip()


def parsed_title_and_author(text):
    '''Extract a title and authors (if present) from the given text string.'''
    title = None
    author = None
    if text.find('/') > 0:
        start = text.find('/')
        title = text[:start].strip()
        author = text[start + 3:].strip()
    elif text.find('[by]') > 0:
        start = text.find('[by]')
        title = text[:start].strip()
        author = text[start + 5:].strip()
    elif text.rfind(', by') > 0:
        start = text.rfind(', by')
        title = text[:start].strip()
        author = text[start + 5:].strip()
    else:
        title = text
    if title.endswith(':'):
        title = title[:-1].strip()
    return title, author
