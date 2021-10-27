from django.shortcuts import render
from .models import ShoeItem
from django.views.generic import View, TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class FAQView(TemplateView):
    template_name = 'faq.html'

class LoginView(TemplateView):
    template_name = 'login.html'

class RegistrationView(TemplateView):
    template_name = 'registration.html'

class ShoppingCartView(TemplateView):
    template_name = 'shopping-cart.html'

class EngageView(TemplateView):
    template_name = 'engage.html'

class SustainabilityView(TemplateView):
    template_name = 'sustainability.html'

class TermsView(TemplateView):
    template_name = 'terms.html'




