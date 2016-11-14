from pygci import GCivicInfo, GCivicInfoError

# Optionally accept user data from the command line
#
# Usage: lookup_representative.py 62701

import sys

if len(sys.argv) >= 2:
    address = sys.argv[1]
else:
    address = raw_input("Voter's address: ")
    # For Python 3.x use: address = input("Voter's address: ")

CivicInfo = GCivicInfo(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

try:
    CivicInfo.get_representative_by_address(address=address)
except GCivicInfoError as e:
    print(e)
