import os

import sys
if sys.version_info[0] == 2 and sys.version_info[1] == 6:
    import unittest2 as unittest
else:
    import unittest

app_key = os.environ.get('APP_KEY')
app_secret = os.environ.get('APP_SECRET')
oauth_token = os.environ.get('OAUTH_TOKEN')
oauth_token_secret = os.environ.get('OAUTH_TOKEN_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
