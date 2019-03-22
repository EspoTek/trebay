import csv

def convertFromTurboListerToTradingApi(turboListerFields):
    tradingApiFormat = dict()
    return tradingApiFormat

def loadFile(filePath):
    parsedData = list()
    with open(filePath, mode='r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            parsedData.append(row)
    
    return parsedData
