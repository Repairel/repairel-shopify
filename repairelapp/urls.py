from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = 'repairelapp'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('about/', AboutView.as_view(), name="about"),
    path('faq/', FAQView.as_view(), name="faq"),
    path('login/', LoginView.as_view(), name="login"),
    path('registration/', RegistrationView.as_view(), name="registration"),
    path('shopping-cart/', ShoppingCartView.as_view(), name="shopping-cart"),
    path('engage/', EngageView.as_view(), name="engage"),
    path('sustainability/', SustainabilityView.as_view(), name="sustainability"),
    path('terms/', TermsView.as_view(), name="terms"),
    path('request/', RequestView.as_view(), name="request"),
    path('gdpr/', GDPRView.as_view(), name="gdpr"),
    path('<pk>/', IndexView.as_view(), name="index"),
]