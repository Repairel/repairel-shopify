from django.urls import (resolve,
                         reverse,
                        )

from django.test import (TestCase,
                         Client,
                        )

from django.utils import timezone
from django.test.utils import setup_test_environment
                         
from repairelapp.models import ShoeItem
from repairelapp.views import (ShoppingCartView,
                               IndexView,
                               )

from repairelapp import shopify
import shopify, requests, time, datetime

from repairelapp.access_keys import get_keys
SHOPIFY_API_KEY, SHOPIFY_API_PASSWORD, REPAIREL_API_KEY, REPAIREL_API_KEY = get_keys()

shopify_api = 'https://%s:%s@repairel-dev.myshopify.com/admin/api/2021-10/' % (SHOPIFY_API_KEY, SHOPIFY_API_PASSWORD)

client=Client()

def create_shoe(title, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return ShoeItem.objects.create(title=title, created=time)

def connect():
    shop_url = "repairel-dev.myshopify.com"
    api_version = '2020-10'
    session = shopify.Session(shop_url, api_version, SHOPIFY_API_PASSWORD)
    shopify.ShopifyResource.activate_session(session)
    
def create_customer_subscriber():
    customer = shopify.Customer()
    customer.email = "subscribertest@gmail.com"
    customer.accepts_marketing = True
    customer = customer.save()

class HomePageTest(TestCase):
    def test_resolve_to_index_page_view(self):
        resolver = resolve('/')
        self.assertEqual(resolver.func.__name__, IndexView.as_view().__name__)
        

class ShoppingCartPageTest(TestCase):
    def test_resolve_to_shopping_cart_page_view(self):
        resolver = resolve('/shopping_cart/')
        self.assertEqual(resolver.func.__name__, ShoppingCartView.as_view().__name__)


class ShoeItemModelTests(TestCase):
    def test_was_published_recently_with_future_shoe_item(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_shoe_item = ShoeItem(created=time)
        self.assertIs(future_shoe_item.was_published_recently(), False)
         
    def test_was_published_recently_with_old_shoe_item(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_shoe_item = ShoeItem(created=time)
        self.assertIs(old_shoe_item.was_published_recently(), False)
        
    def test_was_published_recently_with_recent_shoe_item(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_shoe_item = ShoeItem(created=time)
        self.assertIs(recent_shoe_item.was_published_recently(), True)
        
    def test_was_updated_recently_with_future_shoe_item(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_shoe_item = ShoeItem(updated=time)
        self.assertIs(future_shoe_item.was_updated_recently(), False)
         
    def test_was_updated_recently_with_old_shoe_item(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_shoe_item = ShoeItem(updated=time)
        self.assertIs(old_shoe_item.was_updated_recently(), False)
        
    def test_was_updated_recently_with_recent_shoe_item(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_shoe_item = ShoeItem(updated=time)
        self.assertIs(recent_shoe_item.was_updated_recently(), True)


class Shopify(TestCase):        
    def test_session_connected_successfully(self):
        connect()
        shop = shopify.Shop.current()
        self.assertEqual(shopify.Shop.current().id, shop.get_id())
        
    def test_products_json(self):
        r = requests.get(shopify_api + "products.json")
        self.assertEqual(r.status_code, 200)
        
    def test_blog_json(self):
        r = requests.get(shopify_api + "blogs.json")
        self.assertEqual(r.status_code, 200)
    
    def test_articles_json(self):
        r = requests.get(shopify_api + "articles.json")
        self.assertEqual(r.status_code, 200)
    
    def test_pages_json(self):
        r = requests.get(shopify_api + "pages.json")
        self.assertEqual(r.status_code, 200)
        
    def test_customers_json(self):
        r = requests.get(shopify_api + "customers.json")
        self.assertEqual(r.status_code, 200)
        
    def test_created_customer_of_correct_type(self):
        connect()
        customer = shopify.Customer()
        self.assertIsInstance(customer, shopify.resources.customer.Customer)
        
# class ShopifyProduct:
#     def __init__(self, id, name, description, thumbnail, images, price, tags, product_type, vendor, exact_sizes, colors, condition, gender, group, material, options, variants, extra_info=None):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.thumbnail = thumbnail
#         self.images = images
#         self.price = price
#         self.tags = tags
#         self.product_type = product_type
#         self.vendor = vendor
#         self.options = options
#         self.variants = variants
#         self.extra_info = extra_info
#         self.sizes : list[float] = exact_sizes
#         self.colors = colors
#         self.material = material
        # Below not needed to be tested
#         self.condition = condition
#         self.gender = gender
#         self.group = group
from repairelapp.shopify import ShopifyProduct, _shopify_construct_product
import json
class ProductDeserialiser(TestCase):
    __product : ShopifyProduct = None
    def setUpClass():
        with open("repairelapp\mini.json") as fd:
            obj:dict = json.load(fd)
        ProductDeserialiser.__product = _shopify_construct_product(obj["products"][0])
        
    def tearDownClass(): 
        pass
    
    def test_present(self):
        self.assertIsNotNone(ProductDeserialiser.__product)
        self.assertIsInstance(ProductDeserialiser.__product, ShopifyProduct)
    def test_id(self):
        self.assertEqual(ProductDeserialiser.__product.id, 7547817984231)
    def test_name(self):
        self.assertEqual(ProductDeserialiser.__product.name, "Juta Shoes @ Birdsong- Green Marble Reclaimed Leather Crossover Sandal Women")
    def test_price(self):
        # Fix: make SP.price a number, not a string
        self.assertEqual(ProductDeserialiser.__product.price, "42.00")
    def test_size(self):
        self.assertListEqual(ProductDeserialiser.__product.sizes, ["35","36","42"])
    def test_position(self):
        self.assertEqual(ProductDeserialiser.__product.description, "this is a gray hat description example test")
    def test_vendor(self):
        self.assertEqual(ProductDeserialiser.__product.vendor, "Birdsong")
    def test_image(self):
        self.assertGreaterEqual(len(ProductDeserialiser.__product.images), 1)
        self.assertTrue(ProductDeserialiser.__product.images[0].startswith("https"))
    # def test_tag(self):
    #     self.assertListEqual(ProductDeserialiser.__product.tags, ["Adults", "Birdsong", "Green", "Leather", "New", "Sandals", "Women"])
    # def test_pro
    