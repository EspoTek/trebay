import csv
import xmltodict
import xml.etree.ElementTree

def cleanDict(dictionary):
    hitList = list()
    # Remove "None"s recursively
    for key, value in dictionary.items():
        if type(value) is dict:
            dictionary[key] = cleanDict(value)
        else:
            if value is None:
                hitList.append(key)

    # Delete empty dictionaries cleaned in the loop above
    for key, value in dictionary.items():
        if type(value) is dict and len(value.keys()) == 0:
            hitList.append(key)
      
    for key in hitList:
        del dictionary[key]

    return dictionary

def toBool(field):
    if field is None:
        return None
    elif field == '0':
        return "false"
    elif field == '1':
        return "true"
    else:
        raise RuntimeError("Cannot convert to bool")

def toNameValueList(field, root):
    xmldict = xmltodict.parse(field, dict_constructor=dict)
    return xmldict[root]

def toListingType(turboListerFormat):
    if turboListerFormat == '9':
        return "FixedPriceItem"
    else:
        return None

# TODO:
# Item.BuyerRequirementDetails
# Item.CategoryMappingAllowed 
# Item.Charity 
# Item.CrossBorderTrade
# Item.Currency 
# Item.DigitalGoodInfo
# Item.DisableBuyerRequirements 
# Item.DiscountPriceInfo
# Item.DispatchTimeMax
# Item.eBayPlus 
# Item.HitCounter
# Item.IncludeRecommendations
# Item.InventoryTrackingMethod 
# Item.ItemCompatibilityList
# Item.ListingDesigner
# Item.ListingDetails
# Item.Location
# Item.PaymentMethods
# Item.PayPalEmailAddress
# Item.PickupInStoreDetails 
# Item.PictureDetails 

def convertFromTurboListerToTradingApi(turboListerFields):
    # Default value in turbo lister format is "~"
    for key, value in turboListerFields.items():
        if value == '~':
            turboListerFields[key] = None

    tradingApiFormat = dict()
    itemRoot = dict()
    itemRoot["AutoPay"] = toBool(turboListerFields["AutoPay"])
    
    bestOfferDetails = dict()
    bestOfferDetails["BestOfferEnabled"] = toBool(turboListerFields["BestOfferEnabled"])
    itemRoot["BestOfferDetails"] = bestOfferDetails

    itemRoot["ConditionDescription"] = turboListerFields["ConditionDescription"]
    itemRoot["ConditionID"] = turboListerFields["Condition"]
    itemRoot["Country"] = turboListerFields["Location - Country"]
    itemRoot["Description"] = turboListerFields["Description"]
    itemRoot["ItemSpecifics"] = toNameValueList(turboListerFields["SellerTags"], "ItemSpecifics")
    itemRoot["ListingDuration"] = turboListerFields["Duration"]
    itemRoot["ListingType"] = toListingType(turboListerFields["Format"])

    tradingApiFormat["Item"] = cleanDict(itemRoot)
    
    return tradingApiFormat

def loadFile(filePath):
    parsedData = list()
    with open(filePath, mode='r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            parsedData.append(convertFromTurboListerToTradingApi(row))
    
    return parsedData
