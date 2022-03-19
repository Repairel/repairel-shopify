from re import S
from django.urls import (resolve,
                         reverse,
                        )

from django.test import (TestCase,
                         Client,
                        )

from django.utils import timezone
from django.test.utils import setup_test_environment
                         
from repairelapp.models import ShoeItem
from repairelapp.views import (AllBlogsView, 
                               AllPagesView, 
                               IndexView, 
                               NewsLetterView,
                               ShoesView,
                               translate, shopify_all_products,
                              )
                               
from repairelapp import shopify
from repairelapp.shopify import (ShopifyProduct, _shopify_construct_product,
                                 Page, _shopify_construct_page,
                                 BlogPost, _shopify_construct_article,
                                 Customer, _shopify_construct_customer, all_customers,
                                ) 

import json
import shopify, requests, time, datetime


from repairelapp.access_keys import get_keys
SHOPIFY_API_KEY, SHOPIFY_API_PASSWORD, REPAIREL_API_KEY, REPAIREL_API_PASSWORD = get_keys()

shopify_api = 'https://%s:%s@repairel-dev.myshopify.com/admin/api/2021-10/' % (SHOPIFY_API_KEY, SHOPIFY_API_PASSWORD)

client=Client()

def load_json(file_name):
    with open(file_name) as fd:
        obj:dict = json.load(fd)

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
    def setUp(self):
           self.client = Client()
           self.page_url = reverse('repairelapp:page', kwargs={"page_name":"About"})    
           self.page_url_not_created = reverse('repairelapp:page', kwargs={"page_name":"Non-existen"})    
           self.pages_url = reverse('repairelapp:pages')
           self.shoe_url = reverse('repairelapp:shoe', kwargs={"shoe_id":7538366611687})
           self.shoes_url = reverse('repairelapp:product')
           self.blog_url = reverse('repairelapp:blog', kwargs={"blog_name":"Test post"})
           self.blogs_url = reverse('repairelapp:all_blogs')
           self.newsletter_url = reverse('repairelapp:newsletter')
           self.customer = Customer(id=6134810869996, email="thisissomeemail@gmail.com", accepts_marketing=True)
           self.customers = all_customers()
           
    def test_index_page(self):
       url = reverse('repairelapp:index')
       response = self.client.get(url)
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, 'index.html')
       self.assertContains(response, 'The one stop shop for sustainable footwear')
       
    def test_resolve_to_index_page_view(self):
        resolver = resolve('/')
        self.assertEqual(resolver.func.__name__, IndexView.as_view().__name__)
    def test_resolve_to_blog_page_view(self):
        resolver = resolve('/blogs/')
        self.assertEqual(resolver.func.__name__, AllBlogsView.as_view().__name__)
    def test_resolve_to_pages_view(self):
        resolver = resolve('/pages/')
        self.assertEqual(resolver.func.__name__, AllPagesView.as_view().__name__)
    def test_resolve_to_newsletter_view(self):
        resolver = resolve('/newsletter/')
        self.assertEqual(resolver.func.__name__, NewsLetterView.as_view().__name__)
    
    def test_page_view_GET(self):
        response = client.get(self.page_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'page.html')
        response = client.get(self.page_url_not_created)
        self.assertEquals(response.status_code, 404)
        
    def test_all_pages_view_GET(self):
        response = client.get(self.pages_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages.html')
        self.assertGreaterEqual(len(response.context['pages']), 1)
        
    def test_shoe_view_GET(self):
        response = client.get(self.shoe_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'shoe.html')
        
    def test_blog_view_GET(self):
        response = client.get(self.blog_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog.html')
    
    def test_all_blogs_view_GET(self):
        response = client.get(self.blogs_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_blogs.html')
        
    def test_newsletter_view_GET(self):
        response = client.get(self.newsletter_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        
    def test_newsletter_view_POST_adds_new_subscriber(self):
        connect()
        Customer(id=6134810869996, email="thisissomeemail@gmail.com", accepts_marketing=True)
        
        response = self.client.post(self.newsletter_url, {
            'id':6134810869996,
            'email':'thisissomeemail@gmail.com', 
            'accepts_marketing':True
            })
        
        self.assertEquals(response.status_code, 302)
        
    def test_shoes_view_GET(self):
        response = client.get(self.shoes_url)
        filters = ["new", "refurbished", "women", "men", "unisex", "kids", "other", "shoe"]
        for tag in filters:
            search_tag = translate(tag)
        items = shopify_all_products()
        items = [item for item in items if search_tag in item.tags]
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'shoes.html')
        self.assertIn("New", items[1].tags, f"{items[1].tags}")
        self.assertEquals(items[1].tags, 'Adults, Birdsong, Green, Leather, New, Sandals, Shoe, Women')
        

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


class ProductDeserialiser(TestCase):
    __product : ShopifyProduct = None
    def setUpClass():
        with open("repairelapp/deserialiser_tests/mini_product.json") as fd:
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
        self.assertEqual(ProductDeserialiser.__product.price, "42.00")
        
    def test_size(self):
        self.assertListEqual(ProductDeserialiser.__product.sizes, ["35","36","42"])
        
    def test_color(self):
        self.assertListEqual(ProductDeserialiser.__product.colors, ["Green Marble", "Forest Green", "Turquoise", "Aubergine", "Umber"])
        
    def test_position(self):
        self.assertEqual(ProductDeserialiser.__product.description, "this is a gray hat description example test")
        
    def test_vendor(self):
        self.assertEqual(ProductDeserialiser.__product.vendor, "Birdsong")
        
    def test_image(self):
        self.assertGreaterEqual(len(ProductDeserialiser.__product.images), 1)
        self.assertTrue(ProductDeserialiser.__product.images[0].startswith("https"))
        
    def test_tag(self):
        self.assertEqual(ProductDeserialiser.__product.tags, "Adults, Birdsong, Green, Leather, New, Sandals, Women")
        
    def test_product_type(self):
        self.assertEqual(ProductDeserialiser.__product.product_type, "Sandals")


class PageDeserialiser(TestCase):
    __page : Page = None
    def setUpClass():
        with open("repairelapp/deserialiser_tests/mini_page.json") as fd:
            obj:dict = json.load(fd)
        PageDeserialiser.__page = _shopify_construct_page(obj["pages"][0])
        
    def tearDownClass(): 
        pass
    
    def test_present(self):
        self.assertIsNotNone(PageDeserialiser.__page)
        self.assertIsInstance(PageDeserialiser.__page, Page)
        
    def test_id(self):
        self.assertEqual(PageDeserialiser.__page.id, 100153327847)
    
    def test_title(self):
        self.assertEqual(PageDeserialiser.__page.body, "Meet the REPAIREL team!")
        
    def test_body(self):
        self.assertEqual(PageDeserialiser.__page.title, "Team")


class ArticleDeserialiser(TestCase):
    __article : BlogPost = None
    def setUpClass():
        with open("repairelapp/deserialiser_tests/mini_article.json") as fd:
            obj:dict = json.load(fd)
        ArticleDeserialiser.__article = _shopify_construct_article(obj["articles"][0])
        
    def tearDownClass(): 
        pass
    
    def test_present(self):
        self.assertIsNotNone(ArticleDeserialiser.__article)
        self.assertIsInstance(ArticleDeserialiser.__article, BlogPost)
    
    def test_title(self):
        self.assertEqual(ArticleDeserialiser.__article.title, "Test post")
        
    def test_body(self):
        self.assertEqual(ArticleDeserialiser.__article.body, "Test blog post to see how it interacts with the API")
        
    def test_date_published(self):
        expected_date = "2022-02-13T13:44:52+00:00"
        y, m, d, t = expected_date[:4], expected_date[5:7], expected_date[8:10], expected_date[11:16]
        date = str(f'Published: {d}/{m}/{y}')
        self.assertEqual(ArticleDeserialiser.__article.date, date)
        
    def test_excerpt(self):
        self.assertEqual(ArticleDeserialiser.__article.excerpt, "Excerpt, do you work?")
    
    def test_image(self):
        self.assertGreaterEqual(len(ArticleDeserialiser.__article.image), 1)
        self.assertTrue(ArticleDeserialiser.__article.image.startswith("https")) 
    
    
class CustomerDeserialiser(TestCase):
    __customer : Customer = None
    def setUpClass():
        with open("repairelapp/deserialiser_tests/mini_customer.json") as fd:
            obj:dict = json.load(fd)
        CustomerDeserialiser.__customer = _shopify_construct_customer(obj["customers"][0])
        
    def tearDownClass(): 
        pass
    
    def test_present(self):
        self.assertIsNotNone(CustomerDeserialiser.__customer)
        self.assertIsInstance(CustomerDeserialiser.__customer, Customer)
        
    def test_id(self):
        self.assertEqual(CustomerDeserialiser.__customer.id, 6135297769703)
        
    def test_id(self):
        self.assertEqual(CustomerDeserialiser.__customer.id, 6135297769703)
        
    def test_email(self):
        self.assertEqual(CustomerDeserialiser.__customer.email, "thisissomeemail@mail.com")
        
    def test_email(self):
        self.assertEqual(CustomerDeserialiser.__customer.accepts_marketing, True)
        