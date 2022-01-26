import requests
try:
    from repairelapp import keys
except:
    #TODO pull keys from environment variables
    keys = {
        "API_KEY": '',
        "API_SECRET": '',
    }
    print("keys not found")

url = 'https://%s:%s@repairel-dev.myshopify.com/admin/api/2021-10/' % (keys.API_KEY, keys.PASSWORD)

def get_products():
    endpoint = 'products.json'
    r = requests.get(url + endpoint)
    return r.json()
