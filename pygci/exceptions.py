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
