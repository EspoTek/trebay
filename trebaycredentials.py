import os
import sys
import pathlib

credentialsDir = os.path.join(pathlib.Path.home(), "trebay", "credentials")
ebayCredentials = os.path.join(credentialsDir, "ebay.yaml")

def setCloudinaryCredentials():
    sys.path.append(credentialsDir)
    import cloudinarycredentials