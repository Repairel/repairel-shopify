from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from .shopify import api_view
app_name = 'repairelapp'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/', ShoesView.as_view(), name="product"),
    path('blogs/', AllBlogsView.as_view(), name="all_blogs"),
    path('blog/<str:blog_name>', BlogView.as_view(), name="blog"),
    path('pages/', AllPagesView.as_view(), name="pages"),
    path('pages/<str:page_name>', PageView.as_view(), name="page"),
    path('newsletter/', NewsLetterView.as_view(), name="newsletter"),

    #this is a path for our api
    path('api/local/update_cart/', api_local_update_cart_view, name="api_local_update_cart"),
    path('api/local/<str:request_type>/<str:argument>/', api_local_view, name="api_local"),
    path('api/local/<str:request_type>/', api_local_view, name="api_local"),
    path('api/<str:key>/<str:password>/<str:request_type>/<str:argument>/', api_view, name="api"),
    path('api/<str:key>/<str:password>/<str:request_type>/', api_view, name="api"),

    path('404/', Error404View.as_view(), name="404"),

    #this has to be last
    path('<str:shoe_id>/', ShoeView.as_view(), name="shoe"),

]