from django.urls import resolve
from django.test import TestCase
from repairelapp.models import ShoeItem
from repairelapp.views import (IndexView, 
                               AboutView,
                               FAQView,
                               LoginView,
                               RegistrationView,
                               ShoppingCartView,
                               EngageView,
                               SustainabilityView,
                               TermsView,
                               RequestView,
                               GDPRView,
                               ScoringView,
                               
                               )

# Create your tests here.


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
     
        
class LoginPageTest(TestCase):
    def test_resolve_to_login_page_view(self):
        resolver = resolve('/login/')
        self.assertEqual(resolver.func.__name__, LoginView.as_view().__name__)
        
        
class RegistrationPageTest(TestCase):
    def test_resolve_to_registration_page_view(self):
        resolver = resolve('/registration/')
        self.assertEqual(resolver.func.__name__, RegistrationView.as_view().__name__)
        

class FAQPageTest(TestCase):
    def test_resolve_to_faq_page_view(self):
        resolver = resolve('/faq/')
        self.assertEqual(resolver.func.__name__, FAQView.as_view().__name__)
        

class ShoppingCartPageTest(TestCase):
    def test_resolve_to_shopping_cart_page_view(self):
        resolver = resolve('/shopping_cart/')
        self.assertEqual(resolver.func.__name__, ShoppingCartView.as_view().__name__)
        
        
class EngagePageTest(TestCase):
    def test_resolve_to_engage_page_view(self):
        resolver = resolve('/engage/')
        self.assertEqual(resolver.func.__name__, EngageView.as_view().__name__)
        
     
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
        
         
class RequestPageTest(TestCase):
    def test_resolve_to_request_page_view(self):
        resolver = resolve('/request/')
        self.assertEqual(resolver.func.__name__, RequestView.as_view().__name__)
        
  
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
        