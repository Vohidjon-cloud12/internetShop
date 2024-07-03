from django.contrib import admin
from django.urls import path
from shop.views import home, details, product_of_category, about, add_comment, add_order, add_product, edit_product, \
    delete_product, login_page, logout_page, register

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:product_id>/', details, name='product_detail'),
    path('category/<int:category_id>/', product_of_category, name='category'),
    path('about', about, name='about'),
    path('comments/<int:product_id>', add_comment, name='comments' ),
    path('order/<int:product_id>/', add_order, name='add_order'),
    path('add-product/', add_product, name='add_product'),
    path('update-product/<int:product_id>/', edit_product, name='update-product'),
    path('delete-product<int:product_id>/', delete_product, name='delete-product'),
    path('login', login_page, name='login'),
    path('logout', logout_page, name='logout'),
    path('register', register, name='register'),
]
