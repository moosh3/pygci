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
        return self.requests.get('/elections', params=params)

    def get_voter_info_query(self, address, **params):
        """Looks up information relevant to a voter
        based on the voter's registered address

        :param address: (string) [required]
        :param electionId: (optional) type=long
        :param officialOnly: (optional) type=boolean, default=False
        """
        if 'address' not in params:
            raise GCivicInfoError('This method requires a voters address')
        else:
            return self.get('/voterinfo', params=params)

    # Representatives
    def get_representative_by_address(self, **params):
        """Looks up political geography and representative
        information for a single address

        :param address: (optional) type=string
        :param includeOffices: (optional) type=boolean, default=True
        """
        return self.get('/representatives', params=params)

    def get_representative_by_division(self, ocdId, **params):
        """Looks up representative information for a single
        geographic division

        :param ocdId: type=string
        """
        return self.get('/representatives/%s' % ocdId, params=params)

    # Divisions
    def get_division(self, **params):
        """Searches for political divisions by their
        natural name or OCD ID

        :param query: type=string
        """
        return self.get('/divisions', params=params)
