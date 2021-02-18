'''
record.py: the TindRecord object class for Topi

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

import json
from   json import JSONDecodeError

if __debug__:
    from sidetrack import log

from .tind_utils import result_from_api
from .exceptions import TopiError


# Constants.
# .............................................................................

# URL template for thumbnail images. The result is returned as JSON.
# The first placeholder is for the host URL; the second is for a TIND record id.
# Use Python .format() to substitute the relevant values into the string.
_THUMBNAIL_FOR_TIND_ID = '{}/nanna/thumbnail/{}'


# Class definitions.
# .............................................................................

class TindRecord():
    '''Object class for representing a record from TIND.'''

    # The reason for an explicit list of fields here is so that we can use it
    # in the definition of __repr__().
    __fields = {
        'tind_id'       : str,          # Tind id == MARC control field 001
        'tind_url'      : str,          # Page for the record in TIND
        'title'         : str,          # MARC data field 245
        'subtitle'      : str,          # MARC data field 245
        'author'        : str,          # MARC data field 245 or 100
        'edition'       : str,          # MARC data field 250
        'year'          : str,          # extracted from control field 008
        'isbn_issn'     : list,         # MARC data field 020
        'description'   : str,          # MARC data field 300 concatenated
        'bib_note'      : str,          # MARC data field 504a
        'thumbnail_url' : str,          # Cover image shown on TIND record page
        'items'         : list,         # list of TindItem objects
    }


    def __init__(self, server_url = None, **kwargs):
        # Always first initialize every field.
        for field, field_type in self.__fields.items():
            setattr(self, field, ([] if field_type == list else ''))
        # Set values if given arguments.
        for field, value in kwargs.items():
            setattr(self, field, value)

        # Internal variables.
        self._server_url = server_url
        self._saved_thumbnail_url = None


    def __getattribute__(self, attr):
        if attr == 'thumbnail_url':
            if self._saved_thumbnail_url is not None:
                return self._saved_thumbnail_url
            if __debug__: log(f'getting thumbnail url')
            self._saved_thumbnail_url = self._thumbnail_for_record()
            return self._saved_thumbnail_url
        return object.__getattribute__(self, attr)


    def __str__(self):
        details = f' {self.url}' if self.url else ''
        return f'TindRecord{details}'


    def __repr__(self):
        field_values = []
        for field in self.__fields.keys():
            value = getattr(self, field, None)
            if value:
                if isinstance(value, list):
                    field_values.append(f'{field}={value}')
                else:
                    field_values.append(f'{field}="{value}"')
        if field_values:
            return 'TindRecord(' + ', '.join(field_values) + ')'
        else:
            return 'TindRecord()'


    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return NotImplemented


    def __ne__(self, other):
        # Based on lengthy Stack Overflow answer by user "Maggyero" posted on
        # 2018-06-02 at https://stackoverflow.com/a/50661674/743730
        eq = self.__eq__(other)
        if eq is not NotImplemented:
            return not eq
        return NotImplemented


    def __lt__(self, other):
        return self.tind_id < other.tind_id


    def __gt__(self, other):
        if isinstance(other, type(self)):
            return other.tind_id < self.tind_id
        return NotImplemented


    def __le__(self, other):
        if isinstance(other, type(self)):
            return not other.tind_id < self.tind_id
        return NotImplemented


    def __ge__(self, other):
        if isinstance(other, type(self)):
            return not self.tind_id < other.tind_id
        return NotImplemented


    def _thumbnail_for_record(self, retry = 0):
        '''Return the URL for the thumbnail in TIND for this record.'''
        def response_handler(resp):
            if not resp:
                if __debug__: log(f'got empty json for thumbnail for {self.tind_id}')
                return ''
            try:
                data = json.loads(resp.text)
            except JSONDecodeError as ex:
                raise TindError(f'Malformed result from {self._server_url}: str(ex)')
            except TypeError as ex:
                raise TopiError('Error getting thumbnail -- please report this.')
            if data:
                if 'big' in data:
                    if __debug__: log(f'thumbnail for {self.tind_id} is {data["big"]}')
                    return data['big']
                elif 'small' in data:
                    if __debug__: log(f'thumbnail for {self.tind_id} is {data["small"]}')
                    return data['small']
            else:
                if __debug__: log(f'could not find thumbnail for {self.tind_id}')
                return ''

        endpoint = _THUMBNAIL_FOR_TIND_ID.format(self._server_url, self.tind_id)
        return result_from_api(endpoint, response_handler)
