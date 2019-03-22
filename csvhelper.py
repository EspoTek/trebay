# TODO:
# Item.BuyerRequirementDetails
# Item.CategoryMappingAllowed 
# Item.Charity 
# Item.CrossBorderTrade
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
# Item.PictureDetails (extended)
# Item.PrivateListing 
# Item.PrivateNotes 
# Item.ProductListingDetails 
# Item.QuantityInfo 
# Item.ReturnPolicy 
# Item.ScheduleTime
# Item.SellerProvidedTitle 
# Item.ShippingDetails
# Item.ShippingPackageDetails 
# Item.ShippingServiceCostOverrideList 
# Item.SubTitle 
# Item.UseTaxTable 
# Item.UUID 
# Item.Variations
# Item.VATDetails
# Item.VIN
# Item.VRM

import csv
import xml.etree.ElementTree
import xml.sax.saxutils
import urllib.parse
import xmltodict

import imageuploadhelper

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

def toCurrency(field):
    if field == '5':
        return "AUD"

def toNameValueList(field, root):
    xmldict = xmltodict.parse(field, dict_constructor=dict)
    return xmldict[root]

def toListingType(turboListerFormat):
    if turboListerFormat == '9':
        return "FixedPriceItem"
    else:
        return None

def toPictureURLs(field):
    unparsedList = field.split('|', 1)[0]
    unparsedList = unparsedList.replace("\\", "/")
    parsedList = unparsedList.split('*')[:-1]

    pictureURLs = list()
    for picture in parsedList:
        print("Uploading image %s" % picture)
        pictureURLs.append(imageuploadhelper.upload(picture))
        
    return pictureURLs

def toSite(siteID):
    if siteID == '15':
        return "Australia"
    else:
        return None

def convertFromTurboListerToTradingApi(turboListerFields):
    # Default value in turbo lister format is "~"
    for key, value in turboListerFields.items():
        if value == '~' or value == "":
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
    itemRoot["Currency"] = toCurrency(turboListerFields["Currency"])
    itemRoot["Description"] = xml.sax.saxutils.escape(urllib.parse.unquote(turboListerFields["Description"]))
    itemRoot["ItemSpecifics"] = toNameValueList(turboListerFields["SellerTags"], "ItemSpecifics")
    itemRoot["ListingDuration"] = turboListerFields["Duration"]
    itemRoot["ListingType"] = toListingType(turboListerFields["Format"])

    pictureDetails = dict()
    pictureDetails["PictureURL"] = toPictureURLs(turboListerFields["Item.ExportedImages"])
    itemRoot["PictureDetails"] = pictureDetails
    
    itemRoot["PostalCode"] = turboListerFields["Zip"]

    primaryCategory = dict()
    primaryCategory["CategoryID"] = turboListerFields["Category 1"]
    itemRoot["PrimaryCategory"] = primaryCategory

    itemRoot["Quantity"] = turboListerFields["Quantity"]

    secondaryCategory = dict()
    secondaryCategory["CategoryID"] = turboListerFields["Category 2"]
    itemRoot["SecondaryCategory"] = secondaryCategory

    sellerProfiles = dict()
    
    sellerPaymentProfile = dict()
    sellerPaymentProfile["PaymentProfileName"] = turboListerFields["ITEM_PAYMENT_POLICYNAME"]
    sellerPaymentProfile["PaymentProfileID"] = turboListerFields["ITEM_PAYMENT_POLICYID"]
    sellerProfiles["SellerPaymentProfile"] = sellerPaymentProfile
    
    sellerReturnProfile = dict()
    sellerReturnProfile["ReturnProfileName"] = turboListerFields["ITEM_RETURN_POLICYNAME"]
    sellerReturnProfile["ReturnProfileID"] = turboListerFields["ITEM_RETURN_POLICYID"]
    sellerProfiles["SellerReturnProfile"] = sellerReturnProfile

    sellerShippingProfile = dict()
    sellerShippingProfile["ShippingProfileName"] = turboListerFields["ITEM_SHIPPING_POLICYNAME"]
    sellerShippingProfile["ShippingProfileID"] = turboListerFields["ITEM_SHIPPING_POLICYID"]
    sellerProfiles["SellerShippingProfile"] = sellerShippingProfile

    itemRoot["SellerProfiles"] = sellerProfiles

    itemRoot["Site"] = toSite(turboListerFields["Site"])
    itemRoot["SiteId"] = turboListerFields["Site"]
    itemRoot["SKU"] = turboListerFields["Custom Label"]
    itemRoot["StartPrice"] = turboListerFields["Starting Price"]

    storefront = dict()
    storefront["StoreCategoryID"] = turboListerFields["Store Category"]
    storefront["StoreCategory2ID"] = turboListerFields["Store Category 2"]
    itemRoot["Storefront"] = storefront

    itemRoot["SubTitle"] = turboListerFields["SubtitleText"]
    itemRoot["Title"] = turboListerFields["Title"]

    tradingApiFormat["Item"] = cleanDict(itemRoot)
    
    return tradingApiFormat

def loadFile(filePath):
    parsedData = list()
    with open(filePath, mode='r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            parsedData.append(convertFromTurboListerToTradingApi(row))
            print("\n")
    
    return parsedData
