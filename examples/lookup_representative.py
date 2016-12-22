from pygci import GCivicInfo, GCivicInfoError

# Optionally accept user data from the command line
#
# Usage: lookup_representative.py 62701
import sys

API_KEY = 'AIzaSyDjz3Y8DzW1s00kIuSFKk_zzo5YlUh314w'

if len(sys.argv) >= 2:
    address = sys.argv[1]
else:
    address = raw_input("Voter's address: ")
    # For Python 3.x use: address = input("Voter's address: ")

CivicInfo = GCivicInfo(api_key=API_KEY)

try:
    CivicInfo.get_representative_by_address(params=address)
except GCivicInfoError as e:
    print(e)
