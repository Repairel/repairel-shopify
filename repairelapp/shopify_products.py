import requests
from repairelapp import keys

url = 'https://%s:%s@repairel-dev.myshopify.com/admin/api/2021-10/' % (keys.API_KEY, keys.PASSWORD)

def get_products():
    endpoint = 'products.json'
    r = requests.get(url + endpoint)
    return r.json()
