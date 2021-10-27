from django.shortcuts import render
from .models import ShoeItem
from django.views.generic import View, TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class FAQView(TemplateView):
    template_name = 'faq.html'