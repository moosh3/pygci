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

    content = self._request(url, method=method, params=params)

    return content

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
