"""
pygci.exceptions

Exceptions specific to the GCivicInfo API
"""


class GCivicInfoError(Exception):
    """Generic error class, used for most GCivicInfo issues.

    from pygci import GCivicInfo, GCivicAuthError, GCivicRateLimitError

    """
    pass
    
class GCivicAuthError(Exception):
    """Raised when you attempt to access a protected resource and it
    fails due to an issue with your authentication

    """
    pass

class GCivicRateLimitError(Exception):
    """Raised when you've hit a rate limit.

    The amount of seconds to retry your request in will be
    appended to the message.

    """
    def __init__(self, msg, error_code, retry_after=None):
        if isinstance(retry_after, int):
            msg = '%s (Retry after %d seconds)' % (msg, retry_after)
        GCivicInfoError.__init__(self, msg, error_code=error_code)

        self.retry_after = retry_after
