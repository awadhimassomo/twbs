from django.contrib import admin
from .models import (
    SiteSettings, 
    HomePageSection, 
    ServiceCard, 
    ProductCategory, 
    Product, 
    Page, 
    Testimonial, 
    ContactInquiry
)

# Site Settings (singleton)
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_title', 'site_description')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url')
        }),
        ('Footer', {
            'fields': ('footer_text',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance of SiteSettings
        return SiteSettings.objects.count() == 0


# Home Page Sections
@admin.register(HomePageSection)
class HomePageSectionAdmin(admin.ModelAdmin):
    list_display = ('section_type', 'title', 'active')
    list_filter = ('active',)


# Service Cards
@admin.register(ServiceCard)
class ServiceCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'active')
    list_editable = ('order', 'active')
    list_filter = ('active',)


# Product Categories
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    search_fields = ('name',)


# Products
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'active', 'order')
    list_filter = ('category', 'active')
    list_editable = ('active', 'order')
    search_fields = ('name', 'description')
    filter_horizontal = ()
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'description', 'image')
        }),
        ('Details', {
            'fields': ('features', 'specifications')
        }),
        ('Display Options', {
            'fields': ('order', 'active')
        }),
    )


# Pages
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'active')
    list_editable = ('active',)
    search_fields = ('title', 'content')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'content')
        }),
        ('SEO', {
            'fields': ('meta_description',)
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Display Options', {
            'fields': ('active',)
        }),
    )


# Testimonials
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'active', 'order')
    list_editable = ('active', 'order')
    list_filter = ('active',)
    search_fields = ('name', 'company', 'quote')


# Contact Inquiries
@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_submitted', 'is_read')
    list_filter = ('is_read', 'date_submitted')
    list_editable = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('date_submitted',)
