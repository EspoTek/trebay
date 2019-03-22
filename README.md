# trebay
This is trebay, a tool I've created for exporting Turbo Lister databases and uploading them to the eBay website.
It was basically created for my own use only, so many, many features are missing (including basic stuff like Auctions and countries that are not Australia!)
Of course, this would be a useful basis for anyone else who wanted to add those features.

To use it, you'll need to set up two files under `$HOME/trebay/credentials` (or `C:\Users\blah\trebay\credentials on Windows`)

The first is `cloudinarycredentials.py`, which contains credentials from your free Cloudinary online account (you'll need to set one up).
It looks like this:
```import cloudinary

cloudinary.config(
  cloud_name = 'foo',  
  api_key = 'bar',  
  api_secret = 'fooBar'  
)
```

The second is `ebay.yaml`, which contains credentials for your eBay Developer API account (again, free but you'll need to set one up).
It looks like this:
```
name: ebay_api_config

api.ebay.com:
    appid: foo
    certid: bar
    devid: fizz
    token: buzz
 ```
 
 Then, once you've got them:
 
 Export a file in Turbo Lister [File->Export Selected Items->Turbo Lister Formatted (CSV)]
 
 `pip install cloudinary`
 
 `pip install ebaysdk`
 
 `pip install xmltodict`
 
 `python3 csvup.py /path/to/turboListerFormatted.csv [--dry/--live]`
 
 I recommend using the `--dry` option on your first run, as it doesn't actually upload anything to eBay (just verifies that it can).
 
 And you're done!
