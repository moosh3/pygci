"""
pygci is a Python library that wraps around the
Google Civic API.

It rids of all abstract components, and has checks for
authentication and network issues.

"""

__author__ = 'Alec Cunningham <aleccunningham96@gmail.com>'
__version__ = '0.1'

from .api import GCivicInfo
from .exceptions import (
    GCivicInfoError,
    GCivicAuthError,
    GCivicRateLimitError
)
