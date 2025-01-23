from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('products', views.product_list, name='list_of_products'),
    path('category/<slug:category_slug>', views.product_list, name='products_by_category'),
    path('product/<slug:product_slug>', views.product_details, name='product_details'),
    path('search/', views.product_search, name='product_search'),
]

