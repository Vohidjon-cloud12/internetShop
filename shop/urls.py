from django.contrib import admin
from django.urls import path
from shop.views import home, details, product_of_category, about, comment_add

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:product_id>/', details, name='product_detail'),
    path('category/<int:category_id>/', product_of_category, name='category'),
    path('about', about, name='about'),
    path('comments/<int:prosuct_id>', comment_add, name='comments' )
]
