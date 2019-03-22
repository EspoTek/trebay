import time
import datetime
import sys

import ebaysdk
import ebaysdk.trading
from ebaysdk.exception import *

import csvhelper
import trebaycredentials

def argvError():
    print("ERROR: Invalid Parameters!\nUsage: python3 %s /path/to/turboListerFormatted.csv [--dry/--live]" % sys.argv[0])
    sys.exit(1)

if len(sys.argv) != 3:
    argvError()

csvPath = sys.argv[1]
if sys.argv[2] == "--dry":
    apiCall = "VerifyAddItem"
    print("\n\nRunning as DRY MODE ONLY - nothing will actually be listed on eBay...")
elif sys.argv[2] == "--live":
    apiCall = "AddItem"
    print("\n\nRunning as LIVE MODE - all listings will immediately go live on eBay!!")
else:
    argvError()

print("Press Ctrl-C to cancel if this is a mistake!")
time.sleep(5)
print("OK, let's go!\n")

listings = csvhelper.loadFile(csvPath)

try:
    for listing in listings:
        item = listing["Item"]
        print("Uploading %s" % item["Title"])

        api = ebaysdk.trading.Connection(config_file=trebaycredentials.ebayCredentials)
        response = api.execute(apiCall, listing)
        print("SUCCESS!\n")

except ebaysdk.exception.ConnectionError as e:
    print(e)
    print(e.response.dict())
    print("\nERROR!\n")
