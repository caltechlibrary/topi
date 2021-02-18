'''
tind_utils.py: common utilities for interacting with TIND.

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
from   commonpy.exceptions import NoContent, ServiceFailure, RateLimitExceeded

if __debug__:
    from sidetrack import log

from .exceptions import *


# Internal Constants.
# .............................................................................

# Time in seconds we pause if we hit the rate limit, and number of times we
# repeatedly wait before we give up entirely.
_RATE_LIMIT_SLEEP = 15
_MAX_SLEEP_CYCLES = 8


# Exported functions.
# .............................................................................

def result_from_api(endpoint, result_producer, retry = 0):
    '''Do HTTP GET on "endpoint" & return results of calling result_producer.'''
    (resp, error) = net('get', endpoint)
    if not error:
        if __debug__: log(f'got result from {endpoint}')
        return result_producer(resp)
    elif isinstance(error, NoContent):
        if __debug__: log(f'got empty content from {endpoint}')
        return result_producer(None)
    elif isinstance(error, RateLimitExceeded):
        retry += 1
        if retry > _MAX_SLEEP_CYCLES:
            raise TindError(f'Rate limit exceeded for {endpoint}')
        else:
            if __debug__: log(f'hit rate limit; pausing {_RATE_LIMIT_SLEEP}s')
            wait(_RATE_LIMIT_SLEEP)
            return result_from_tind(endpoint, result_producer, retry = retry)
    else:
        if __debug__: log(f'got {type(error)} error for {endpoint}')
        raise TindError(f'Problem contacting {endpoint}: {str(error)}')
