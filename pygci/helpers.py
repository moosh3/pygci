"""
pygci.helpers

Functions commonly used throughout the pygci library

Credit to @RyanMcGrath's Twython wrapper:
https://raw.githubusercontent.com/ryanmcgrath/twython/twython/helpers.py
"""

from .compat import basestring, numeric_types


def _transparent_params(_params):
    params = {}
    files = {}
    for k, v in _params.items():
        if hasattr(v, 'read') and callable(v.read):
            files[k] = v  # pragma: no cover
        elif isinstance(v, bool):
            if v:
                params[k] = 'true'
            else:
                params[k] = 'false'
        elif isinstance(v, basestring) or isinstance(v, numeric_types):
            params[k] = v
        elif isinstance(v, list):
            try:
                params[k] = ','.join(v)
            except TypeError:
                params[k] = ','.join(map(str, v))
        else:
            continue  # pragma: no cover
    return params, files
