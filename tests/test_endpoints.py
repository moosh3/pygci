from pygci import GCivicInfo, GCivicInfoError, GCivicAuthError

import time


class GCivicInfoEndpointsTestCase(unittest.TestCase):
    def setUp(self):

        self.api = GCivicInfo(api_key, oauth_token, oauth_token_secret,
                              client_args=client_args)

    # Elections
    def test_get_election_query(self):
        """Test returning list of avaliable elections to query"""
        self.api.get_election_query()

    def test_get_voter_info_query(self):
        """Test return infomation relevant to a voter
        based on the voter's registered address
        """
        self.api.get_voter_info_query(address='Illinois State Capitol, Springfield, IL 62756')

    # Representatives
    def test_get_representatives_by_address(self):
        self.api.get_representative_by_address()

    def test_get_representatives_by_division(self):
        self.api.get_representative_by_division()

    # Divisions
    def test_get_division(self):
        self.api.get_division()
