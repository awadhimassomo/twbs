from django.urls import path
from . import views

app_name = 'adminpage'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.admin_login, name='login'),
    path('signup/', views.admin_signup, name='signup'),
    path('logout/', views.admin_logout, name='logout'),
    
    # Site settings
    path('settings/', views.edit_settings, name='settings'),
    
    # Products management
    path('products/', views.list_products, name='products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    
    # Categories management
    path('categories/', views.list_categories, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    # Testimonials management
    path('testimonials/', views.list_testimonials, name='testimonials'),
    path('testimonials/add/', views.add_testimonial, name='add_testimonial'),
    path('testimonials/edit/<int:pk>/', views.edit_testimonial, name='edit_testimonial'),
    path('testimonials/delete/<int:pk>/', views.delete_testimonial, name='delete_testimonial'),
    
    # Contact inquiries
    path('inquiries/', views.list_inquiries, name='inquiries'),
    path('inquiries/view/<int:pk>/', views.view_inquiry, name='view_inquiry'),
    path('inquiries/mark-read/<int:pk>/', views.mark_inquiry_read, name='mark_inquiry_read'),
    path('inquiries/delete/<int:pk>/', views.delete_inquiry, name='delete_inquiry'),
]
