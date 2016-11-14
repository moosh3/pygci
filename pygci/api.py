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

from oauth2client import client

from . import __version__
from .endpoints import EndpointsMixin
from .exceptions import
    GCivicInfoError,
    GCivicAuthError,
    GCivicRateLimitError
from .helpers import _transparent_params


class GCivicInfo(EndpointsMixin, object):
    def __init__(self, app_key=None, app_secret=None, oauth_token=None,
                 oauth_token_secret=None, oauth_version=2, api_key=None,
                 api_version='v2', client_args=None, auth_enpoint='authenticate'):
        """Creates a new GCivicInfo instance, with option parameters for
        authentication and so forth

        :param app_key: (optional) Your applications key
        :param app_secret: (optional) Your applications secret key
        :param oauth_token: (optional) When using **OAuth 1**, combined with
        oauth_token_secret to make authenticated calls
        :param oauth_token_secret: (optional) When using **OAuth 1** combined
        with oauth_token to make authenticated calls
        :param access_token: (optional) When using **OAuth 2**, provide a
        valid access token if you have one
        :param token_type: (optional) When using **OAuth 2**, provide your
        token type. Default: bearer
        :param oauth_version: (optional) Choose which OAuth version to use.
        Default: 1
        :param api_version: (optional) Choose which GCI API version to
        use. Default: v2

        :param client_args:
        :param auth_endpoint:
        """
        self.api_version = api_version
        self.api_url = 'https://www.googleapis.com/civicinfo/%s/%s'

        self.app_key = app_key
        self.app_secret = app_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

        if oauth_version == 2:
            self.#request a token url

        self.oauth_version = oauth_version

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
        # Using requests package until custom request and _request method are complete
        return self.requests.get(endpoint, params=params, version=version)

    """Authentication setup goes here"""


    @staticmethod
    def construct_api_url(api_url, **params):
        """Creates GCI API url, encoded with parameters

        :param api_url: URL of the GCI API endpoint you are attempting to construct
        :param \*\*params: Parameters accepted by GCI for the specific endpoint
        you are requesting
        """
        querystring = []
        params, _ = _transparent_params(params or {})
        params = requests.utils.to_key_val_list(params)
        for (k, v) in params:
            querystring.append(
                '%s=%s' % (pygci.encode(k), quote_plus(pygci.encode(v)))
            )
        return '%s?%s' % (api_url, '&'.join(querystring))

    @staticmethod
    def unicode2utf8(text):
        try:
            if is_py2 and isinstance(text, str):
                text = text.encode('utf-8')
        except:
            pass
        return text

    @staticmethod
    def encode(text):
        if is_py2 and isinstance(text, (str)):
            return pygci.unicode2utf8(text)
        return str(text)
