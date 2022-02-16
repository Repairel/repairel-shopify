import os, requests
from repairelapp import keys

API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("PASSWORD")

url = f'https://{keys.API_KEY}:{keys.PASSWORD}@repairel-dev.myshopify.com/admin/api/2021-10/'
#print(url)

def get_products():
    #TODO to access metafields use the url: 'products/7461853069543/metafields.json'
    #so 'products/<id>/metafields.json'
    endpoint = "products.json"
    r = requests.get(url + endpoint)
    return r.json()

# get_products = get_products()
# products = get_products['products']
# print(products[3].items())

def get_blog():
    endpoint = "blogs.json"
    r = requests.get(url+endpoint)
    blog = r.json()["blogs"][0]["id"]
    articles = requests.get(url+f"blogs/{blog}/articles.json")
    #print(articles.json())
    return articles.json()["articles"]

print(get_blog())
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
