"""
pygci.exceptions

Exceptions specific to the GCivicInfo API
"""


class GCivicInfoError(Exception):
    pass

class GCivicAuthError(Exception):
    pass

class GCivicRateLimitError(Exception):
    pass
