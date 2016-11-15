"""
pygci.api

API Client for access to GCivicInfo API calls,
GCI authentication, and other methods needed when
dealing with the GCI API
"""

import warnings
import re
import os

import requests
from requests.auth import HTTPBasicAuth

from oauth2client import client

from . import __version__
from .endpoints import EndpointsMixin
from .exceptions import
    GCivicInfoError,
    GCivicAuthError,
from .helpers import _transparent_params


class GCivicInfo(EndpointsMixin, object):
    def __init__(self, api_key=None, oauth_token=None,
                 oauth_token_secret=None, oauth_version=2, api_version='v2',
                 client_args=None, auth_enpoint='authenticate'):
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

        self.api_key = api_key
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

        if oauth_version == 2:
            self.#request a token url

        self.oauth_version = oauth_version

        # requests HEADERS change

    def __repr__(self):
        return '<GCivicInfo: %s>' % (__version__)

    def request(self, endpoint, method='GET', params=None, version='v2'):
        """Let's do some nice python things with the requests packages"""
        if endpoint.startswith('http://'):
            raise GCivicInfoError('www.googleapis.com is restricted to SSL/TLS traffic.')

        # In case the want to pass a full GCI URL
        if endpoint.startswith('https://'):
            url = endpoint
        else:
            url = '%s/%s?key=%s' % (self.api_url % version, endpoint, api_key)

        content = requests.get(url, params=params)

        if 'application/json' not in content.headers['content-type']:
            raise GCivicInfoError("Response was not valid Json")
        else:
            content = content.json()

        return content

    def get(self, endpoint, api_key=api_key, params=None, version='v2'):
        """Shortcut for GET requests"""
        # Using requests package until custom request and _request method are complete
        return self.request(endpoint, api_key, params=params, version=version)
