import datetime

import ebaysdk
import ebaysdk.trading
from ebaysdk.exception import *

import csvhelper

listings = csvhelper.loadFile("/home/esposch/Downloads/sample-gta5.csv")

try:
    for listing in listings:
        item = listing["Item"]
        print("Uploading listing %s" % item["Title"])

        api = ebaysdk.trading.Connection(config_file="/home/esposch/credentials/ebay.yaml")
        response = api.execute('AddFixedPriceItem', listing)
        print(response.dict())
        print(response.reply)
        print("\nSUCCESS!\n")

except ebaysdk.exception.ConnectionError as e:
    print(e)
    print(e.response.dict())
    print("\nERROR!\n")
