import datetime

import ebaysdk
import ebaysdk.trading
from ebaysdk.exception import *

import csvhelper

listings = csvhelper.loadFile("/home/esposch/Downloads/sample-gta5.csv")

print(listings)

try:
    for listing in listings:
        item = listing["Item"]
        print("Uploading listing %s" % item["Title"])

        api = ebaysdk.trading.Connection(config_file="/home/esposch/credentials/ebay.yaml")
        response = api.execute('VerifyAddItem', listing)
        print(response.dict())
        print(response.reply)

except ebaysdk.exception.ConnectionError as e:
    print(e)
    print(e.response.dict())
