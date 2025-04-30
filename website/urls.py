from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<slug:category_slug>/', views.products, name='product_category'),
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('page/<slug:page_slug>/', views.custom_page, name='custom_page'),
]
