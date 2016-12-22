"""
pygci.api

API Client for access to GCivicInfo API calls,
GCI authentication, and other methods needed when
dealing with the GCI API
"""
import requests
from requests_oauthlib import OAuth2


from . import __version__
from .endpoints import EndpointsMixin
from .exceptions import GCivicInfoError


class GCivicInfo(EndpointsMixin, object):
    def __init__(self, api_key=None, oauth_token=None,
                 oauth_token_secret=None, oauth_version=2,
                 access_token=None, token_type='bearer', api_version='v2',
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

        :param auth_endpoint:
        """
        self.api_version = api_version
        self.api_url = 'https://www.googleapis.com/civicinfo/{}/{}'
        self.api_key = api_key

        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.access_token = access_token

        if self.oauth_token:
            oauth_version = 2

        self.oauth_version = oauth_version

        self.client_args = client_args or {}
        default_headers = {'User-Agent': 'pygci v' + __version__}
        if 'headers' not in self.client_args:
            # If they didn't set any headers, set our defaults for them
            self.client_args['headers'] = default_headers
        elif 'User-Agent' not in self.client_args['headers']:
            # If they set headers, but didn't include User-Agent.. set
            # it for them
            self.client_args['headers'].update(default_headers)

        auth = None
        if oauth_version == 2 and self.access_token:
            token = {'token_type': token_type,
                     'access_token': self.access_token}
            auth = OAuth2(self.app_key, token=token)
        else:
            auth = None

        self.client = requests.Session()
        self.client.auth = auth

        # Make a copy of the client args and iterate over them
        # Pop out all the acceptable args at this point because they will
        # Never be used again.
        client_args_copy = self.client_args.copy()
        for k, v in client_args_copy.items():
            if k in ('cert', 'hooks', 'max_redirects', 'proxies'):
                setattr(self.client, k, v)
                self.client_args.pop(k)  # Pop, pop!

        # Headers are always present, so we unconditionally pop them and merge
        # them into the session headers.
        self.client.headers.update(self.client_args.pop('headers'))

        self._last_call = None

    def __repr__(self):
        return '<GCivicInfo: %s>' % (__version__)

    def _request(self, url, method='GET', params=None, api_call=None):
        """Internal request method"""
        method = method.lower()
        params = params or {}

        func = getattr(self.client, method)

        requests_args = {}
        for k, v in self.client_args.items():
            # Maybe this should be set as a class variable and only done once?
            if k in ('timeout', 'allow_redirects', 'stream', 'verify'):
                requests_args[k] = v
        requests_args['params'] = params

        try:
            response = func(url, **requests_args)
        except requests.RequestException as e:
            raise GCivicInfoError(str(e))

        self._last_call = {
                    'api_call': api_call,
                    'api_error': None,
                    'cookies': response.cookies,
                    'headers': response.headers,
                    'status_code': response.status_code,
                    'url': response.url,
                    'content': response.text,
                }
        try:
            if response.status_code == 204:
                content = response.content
            else:
                content = response.json()
        except ValueError:
            raise GCivicInfoError('Response was not valid Json')

        return content

    def request(self, endpoint, params=None, version='v2'):
        """Let's do some nice python things with the requests packages"""
        if endpoint.startswith('http://'):
            raise GCivicInfoError('Restricted to SSL/TLS traffic.')

        # In case the want to pass a full GCI URL
        if endpoint.startswith('https://'):
            url = endpoint
        else:
            url = self.api_url.format(
                version, endpoint) + params + '&key='
        content = self._request(url, method='GET', params=params)

        return content

    def get(self, endpoint='GET', api_key=None, params=None, version='v2'):
        """Shortcut for GET requests"""
        return self.request(endpoint, params=params, version=version)
