from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from .shopify import api_view
app_name = 'repairelapp'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('about/', AboutView.as_view(), name="about"),
    path('faq/', FAQView.as_view(), name="faq"),
    path('login/', LoginView.as_view(), name="login"),
    path('registration/', RegistrationView.as_view(), name="registration"),
    path('shopping_cart/', ShoppingCartView.as_view(), name="shopping_cart"),
    path('engage/', EngageView.as_view(), name="engage"),
    path('sustainability/', SustainabilityView.as_view(), name="sustainability"),
    path('terms/', TermsView.as_view(), name="terms"),
    path('request/', RequestView.as_view(), name="request"),
    path('gdpr/', GDPRView.as_view(), name="gdpr"),
    path('scoring/', ScoringView.as_view(), name="scoring"),
    #path('shopify_items/', ShopifyView.as_view(), name="shopify_items"),
    path('blog/', BlogView.as_view(), name="blog"),

    #this is a path for our api
    path('api/<str:key>/<str:password>/<str:request_type>/<str:argument>/', api_view, name="api"),
    path('api/<str:key>/<str:password>/<str:request_type>/', api_view, name="api"),


    #TODO these. They are not working yet.
    path('product_request/', IndexView.as_view(), name="product_request"),
    path('donate/', IndexView.as_view(), name="donate"),


    #this has to be last
    path('<str:shoe_id>/', ShoeView.as_view(), name="shoe"),

]