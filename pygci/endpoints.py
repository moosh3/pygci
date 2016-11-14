"""
pygci.endpoints

A mixin for a GCivicInfo <GCivicInfo> instance.
Params that need to be embedded in the API url just
need to be passed as a keyboard argument.

e.g. GCivicInfo.representative(address)
"""

import os
import warnings
from io import BytesIO
from time import sleep


class EndpointsMixin(object):
    # Elections
    def get_election_query(self, **params):
        """List of available election to query
        """

    def get_voter_info_query(self, address, **params):
        """Looks up information relevant to a voter
        based on the voter's registered address
        """

    # Representatives
    def get_representative_by_address(self, **params):
        """Looks up political geography and representative
        information for a single address

        params:
            - address, includeOffices, levels, roles
        """

    def get_representative_by_division(self, **params):
        """Looks up representative information for a single
        geographic division
        """

    # Divisions
    def get_division(self, **params):
        """Searches for political divisions by their
        natural name or OCD ID
        """
