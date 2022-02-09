import requests
from repairelapp import keys

url = 'https://%s:%s@repairel-dev.myshopify.com/admin/api/2021-10/' % (keys.API_KEY, keys.PASSWORD)

def get_products():
    #TODO to access metafields use the url: 'products/7461853069543/metafields.json'
    #so 'products/<id>/metafields.json'
    endpoint = "products.json"
    r = requests.get(url + endpoint)
    print(r.json())
    return r.json()
