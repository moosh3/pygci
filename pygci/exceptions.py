"""
pygci.exceptions

Exceptions specific to the GCivicInfo API
"""


class GCivicInfoError(Exception):
    """Generic error class, used for most GCivicInfo issues.

    from pygci import GCivicInfo, GCivicAuthError, GCivicRateLimitError

    """
    def __init__(self, msg, error_code=None, retry_after=None):
        self.error_code = error_code

        if error_code is not None and error_code in CIVIC_INFO_HTTP_STATUS_CODE:
            msg: 'Google Civic Info API return a %s (%s), %s' % \
                (error_code,
                 CIVIC_INFO_HTTP_STATUS_CODE[error_code][0],
                 msg)

        super(GCivicInfoError, self).__init__(msg)

    @property
    def msg(self):
        return self.args[0]

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
