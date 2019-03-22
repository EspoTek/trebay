import sys
import cloudinary
import cloudinary.uploader
import cloudinary.api

sys.path.append('/home/esposch/credentials')
import cloudinarycredentials

def upload(imagePath):
  # http://res.cloudinary.com/trebay56bits/image/upload/test_folder/test.jpg
  response = cloudinary.uploader.upload(imagePath, folder = "ebay", overwrite = False)
  return response["secure_url"]