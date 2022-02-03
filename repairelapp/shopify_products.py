import requests
try:
    from repairelapp import keys
    url = 'https://%s:%s@repairel-dev.myshopify.com/admin/api/2021-10/' % (keys.API_KEY, keys.PASSWORD)
except:
    #TODO pull keys from environment variables
    url = None
    print("keys not found")


def get_products():
    if(url):
        endpoint = 'products.json'
        r = requests.get(url + endpoint)
        return r.json()
    else:
        return ""
