"""
GCivicInfo.Client

API Client for access to GCivicInfo API calls,
GCI authentication, and other methods needed when
dealing with the GCI API
"""

import warnings
import re

import requests
from requests.auth import HTTPBasicAuth
from request_oauthlib import OAuth1, OAuth2

from . import __version__
from .endpoints import EndpointsMixin
from .exceptions import
    GCivicInfoError,
    GCivicAuthError,
    GCivicRateLimitError
from .helpers import _transparent_params


class GCivicInfo(EndpointsMixin, object):
    def __init__(self, app_key=None, app_secret=None, oauth_token=None,
                 oauth_token_secret=None, oauth_version=1, api_key=None,
                 api_version='v2', client_args=None, auth_enpoint='authenticate'):
        """Creates a new GCivicInfo instance, with option parameters for
        authentication and so forth
        """
        self.api_version = api_version
        self.api_url = 'https://www.googleapis.com/civicinfo/%s/%s'

        self.app_key = app_key
        self.app_secret = app_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

        self.client_args - client_args or {}
        default_headers = {'User-Agent': 'GCivicInfo v' + __version__}
        if 'headers' not in self.client_args['headers']:
            # If the set headers but not the User-Agest..
            # set it for them, thanks
            self.client_args['headers'].update(default_headers)

        # Make a copy of the client_args and iterate over them
        # Pop out all the acceptable args because they will
        # never be used again
        client_args_copy = self.client_args.copy()
        for k, v in client_args_copy.items():
            if k in ('cert', 'hooks', 'max_redirects', 'proxies'):
                setattr(self.client, k, v)
                self.client_args.pop(k)

        # Headers are always present, so unconditionally pop them
        # and merge them into the session headers
        self.client.headers.update(self.client_args.pop('headers'))

    def __repr__(self):
        return '<GCivicInfo: %s>' % (self.app_key)

    def _request(self, url, method='GET', params=None, api_call=None):
        """Internal request method"""
        method = method.lower()
        params = params or {}

        func = getattr(self.client, method)
        params, files = _transparent_params(params)

        request_args = {}
        if method == 'get':
            request_args['params'] = params
        else:
            request_args.update({
                'data': params,
                'files': files,
            })
        try:
            response = func(url, **request_args)
        except request.RequestException as e:
            raise GCivicInfoError(str(e))

        try:
            if response.status_code == 204:
                content = response.content
            else:
                content = response.json()
        except ValueError:
            raise GCivicInfoError('Response was not valid JSON. \
                                  Unable to decode.')

        return content

    def request(self, endpoint, method='GET', params=None, version='v2'):
        """Return dict of response from GCI API"""
        if endpoint.startswith('http://'):
            raise GCivicInfoError('www.googleapis.com is restricted to SSL/TLS traffic.')

        # In case the want to pass a full GCI URL
        if endpoint.startswith('https://'):
            url = endpoint
        else:
            url = '%s/%s' % (self.api_url % version, endpoint)

        content = self._request(url, method=method, params=params, api_call=url)

        return content

    def get(self, endpoint, params=None, version='v2'):
        """Shortcut for GET requests"""
        return self.request(endpoint, params=params, version=version)

    def post(self, endpoint, params=None, version='v2'):
        """Shortcut for POST requests"""
        return self.request(endpoint, 'POST', params=params, version=version)

    """Authentication setup goes here"""

    @staticmethod
    def construct_api_url(api_url, **params):
        """Creates GCI API url, encoded with parameters

        Usage:

            >>> from pygci import GCivicInfo
            >>> CivicInfo = GCivicInfo()

            >>> api_url = 'https://www.googleapis.com/civicinfo/v2/elections'
            >>> constructed_url = CivicInfo.construct_api_url(api_url, version, params)
            >>> print(constructed_url)
            https://www.googleapis.com/civicinfo/v2/elections?key=<API_KEY>
        """
        
