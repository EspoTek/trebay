import datetime

import ebaysdk
import ebaysdk.trading
from ebaysdk.exception import *

import csvhelper

listings = csvhelper.loadFile("/home/esposch/Downloads/sample-gta5.csv")
# print(listings)


# try:
#     api = ebaysdk.trading.Connection(config_file="/home/esposch/credentials/ebay.yaml")
#     response = api.execute('GetUser', {})
#     print(response.dict())
#     print(response.reply)

# except ebaysdk.exception.ConnectionError as e:
#     print(e)
#     print(e.response.dict())
