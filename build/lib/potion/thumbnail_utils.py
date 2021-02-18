'''
thumbnail.py: retrieve a cover image.

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from   commonpy.network_utils import net
from   lxml import etree, html

if __debug__:
    from sidetrack import log

def thumbnail_from_amazon(isbn):
    '''Given an ISBN, return a URL for an cover image thumbnail.'''
    (response, error) = net('get', _ISBN_SEARCH_AMAZON.format(isbn))
    if error:
        return None
    # For Amazon, we scrape the results page.
    page = html.fromstring(response.content)
    img_element = page.cssselect('img.s-image')
    if img_element:
        return img_element[0].attrib['src']
    return None


def thumbnail_from_google(isbn):
    '''Given an ISBN, return a URL for an cover image thumbnail.'''
    (response, error) = net('get', _ISBN_SEARCH_GOOGLE.format(isbn))
    if error:
        return None
    # Google returns JSON, making it easier to get data directly.
    json = jsonlib.loads(response.content.decode())
    if 'items' not in json:
        return None
    if 'volumeInfo' not in json['items'][0]:
        return None
    info = json['items'][0]['volumeInfo']
    if 'imageLinks' in info and 'thumbnail' in info['imageLinks']:
        return info['imageLinks']['thumbnail']
    return None
