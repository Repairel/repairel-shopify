from django.urls import (resolve,
                         reverse,
                        )
from django.test import (TestCase,
                         Client,
                        )
                         
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
                               )
import datetime
from django.utils import timezone
from django.test.utils import setup_test_environment




# Create your tests here.
# setup_test_environment()
client=Client()

def create_shoe(title, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return ShoeItem.objects.create(title=title, created=time)

class HomePageTest(TestCase):
    def test_resolve_to_index_page_view(self):
        resolver = resolve('/')
        self.assertEqual(resolver.func.__name__, ShoesView.as_view().__name__)
        
    # def test_no_shoe(self):
    #     response = self.client.get(reverse('repairelapp:index'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "No shoes are available.")
    #     self.assertQuerysetEqual(response.context['latest_list'], [])
    #     self.assertTemplateUsed(response, 'index.html')
        
    # def test_past_shoe(self):
    #     shoe = create_shoe(title="Past shoe.", days=-30)
    #     response = self.client.get(reverse('repairelapp:index'))
    #     self.assertQuerysetEqual(response.context['latest_list'], [shoe])
        
    # def test_two_past_shoes(self):
    #     shoe1 = create_shoe(title="Past shoe 1.", days=-30)
    #     shoe2 = create_shoe(title="Past shoe 2.", days=-5)
    #     response = self.client.get(reverse('repairelapp:index'))
    #     self.assertQuerysetEqual(response.context['latest_list'], [shoe2, shoe1])
        
    # def test_future_shoe(self):
    #     create_shoe(title="Future shoe.", days=30)
    #     response = self.client.get(reverse('repairelapp:index'))
    #     self.assertContains(response, "No shoes are available.")
    #     self.assertQuerysetEqual(response.context['latest_list'], [])
        
    # def test_future_shoe_and_past_shoe(self):
    #     shoe = create_shoe(title="Past shoe.", days=-30)
    #     create_shoe(title="Future shoe.", days=30)
    #     response = self.client.get(reverse('repairelapp:index'))
    #     self.assertQuerysetEqual(response.context['latest_list'], [shoe])
        

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
