import binascii
import os
import shopify
import keys

shopify.Session.setup(api_key=keys.API_KEY, secret=keys.SHARED_SECRET)

shop_url = "repairel_dev.myshopify.com"
api_version = '2021-10'
state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
redirect_uri = "http://127.0.0.1:8000/auth/shopify/callback"
scopes = ['read_products', 'read_orders']

newSession = shopify.Session(shop_url, api_version)
auth_url = newSession.create_permission_url(scopes, redirect_uri, state)
# redirect to auth_url

session = shopify.Session(shop_url, api_version)
access_token = session.request_token() # request_token will validate hmac and timing attacks
# you should save the access token now for future use.

session = shopify.Session(shop_url, api_version, access_token)
shopify.ShopifyResource.activate_session(session)

shop = shopify.Shop.current() # Get the current shop
product = shopify.Product.find(179761209) # Get a specific product

# execute a graphQL call
shopify.GraphQL().execute("{ shop { name id } }")
