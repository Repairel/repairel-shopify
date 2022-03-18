from django.urls import (resolve,
                         reverse,
                        )

from django.test import (TestCase,
                         Client,
                        )

from django.utils import timezone
from django.test.utils import setup_test_environment
                         
from repairelapp.models import ShoeItem
from repairelapp.views import (ShoesView, 
                               AboutView,
                               FAQView,
                               ShoppingCartView,
                               ActivismView,
                               SustainabilityView,
                               TermsView,
                               RequestView,
                               GDPRView,
                               ScoringView, 
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


class AboutPageTest(TestCase):
    def test_resolve_to_about_page_view(self):
        resolver = resolve('/about/')
        self.assertEqual(resolver.func.__name__, AboutView.as_view().__name__)
        
        
class FAQPageTest(TestCase):
    def test_resolve_to_faq_page_view(self):
        resolver = resolve('/faq/')
        self.assertEqual(resolver.func.__name__, FAQView.as_view().__name__)
        

class FAQPageTest(TestCase):
    def test_resolve_to_faq_page_view(self):
        resolver = resolve('/faq/')
        self.assertEqual(resolver.func.__name__, FAQView.as_view().__name__)
        

class ShoppingCartPageTest(TestCase):
    def test_resolve_to_shopping_cart_page_view(self):
        resolver = resolve('/shopping_cart/')
        self.assertEqual(resolver.func.__name__, ShoppingCartView.as_view().__name__)
        
        
class ActivismPageTest(TestCase):
    def test_resolve_to_engage_page_view(self):
        resolver = resolve('/activism/')
        self.assertEqual(resolver.func.__name__, ActivismView.as_view().__name__)
        
     
class SustainabilityPageTest(TestCase):
    def test_resolve_to_faq_page_view(self):
        resolver = resolve('/sustainability/')
        self.assertEqual(resolver.func.__name__, SustainabilityView.as_view().__name__)
        
        
class TermsPageTest(TestCase):
    def test_resolve_to_terms_page_view(self):
        resolver = resolve('/terms/')
        self.assertEqual(resolver.func.__name__, TermsView.as_view().__name__)
        

class FAQPageTest(TestCase):
    def test_resolve_to_faq_page_view(self):
        resolver = resolve('/faq/')
        self.assertEqual(resolver.func.__name__, FAQView.as_view().__name__)
        
  
class GDPRPageTest(TestCase):
    def test_resolve_to_gdpr_page_view(self):
        resolver = resolve('/gdpr/')
        self.assertEqual(resolver.func.__name__, GDPRView.as_view().__name__)
        

class ScoringPageTest(TestCase):
    def test_resolve_to_scoring_page_view(self):
        resolver = resolve('/scoring/')
        self.assertEqual(resolver.func.__name__, ScoringView.as_view().__name__)
        

class PageTest(TestCase):
    def test_resolve_to_faq_page_view(self):
        resolver = resolve('/faq/')
        self.assertEqual(resolver.func.__name__, FAQView.as_view().__name__)


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