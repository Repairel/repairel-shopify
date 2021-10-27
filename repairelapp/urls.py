from django.urls import path
from .views import (IndexView,
                    AboutView,
                    FAQView,
                    )
from django.views.generic import TemplateView


# app_name = 'repairelapp'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('about', AboutView.as_view(), name="about"),
    path('faq', FAQView.as_view(), name="faq"),
]