from pygci import GCivicInfo, GCivicInfoError, GCivicAuthError

from .config import (
    unittest, api_key
)

import responses
import requests

try:
    import unittest.mock as mock
except ImportError:
    import mock


class GCivicInfoAPITestCase(unittest.TestCase):
    def setUp(self):
        self.api = GCivicInfo('','','','')

    def get_url(self, endpoint):
        """Convenience function for mapping from endpoint to URL"""
        return '%s/%s?key=%s' % (self.api.api_url % self.api.api_version, endpoint, api_key)

    def register_response(self, url, method='GET', status=200,
                          content_type='application/json; charset=utf-8'):
        """Wrapper function for responses for simpler unit tests"""
        responses.add(url, status, content_type)

    @responses.activate
    def test_requests_should_handle_full_endpoint(self):
        """Test that requests() accepts a full URL plus endpoint"""
        url = 'https://wwww.googleapis.com/civicinfo/v2/elections
        self.register_response(responses.GET, url)

        self.requests.get(url)

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(url, responses.calls[0])
