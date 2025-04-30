from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator


class SiteSettings(models.Model):
    """Global site settings like contact info and social media links"""
    site_title = models.CharField(max_length=100, default="Twebs")
    site_description = models.TextField(default="Leading supplier of laboratory and scientific instrumentation in Southern Africa")
    email = models.EmailField(default="info@twebs.com")
    phone = models.CharField(max_length=20, default="+27 123 456 789")
    address = models.TextField(default="123 Lab Street, Pretoria, South Africa")
    
    # Social media links
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    # Footer text
    footer_text = models.CharField(max_length=200, default="  Twebs 2025. All Rights Reserved.")
    
    def __str__(self):
        return "Site Settings"
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"


class HomePageSection(models.Model):
    """Sections on the homepage like hero, services, why us"""
    SECTION_TYPES = (
        ('hero', 'Hero Section'),
        ('services', 'Services Section'),
        ('why_us', 'Why Choose Us Section'),
    )
    
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, unique=True)
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.get_section_type_display()


class ServiceCard(models.Model):
    """Cards in the services section"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, help_text="Name of the SVG icon to use")
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order']


class ProductCategory(models.Model):
    """Categories for products like Air Filter, Mask Systems, etc."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, editable=False)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Product Categories"
        ordering = ['order']


class Product(models.Model):
    """Individual products"""
    category = models.ForeignKey(ProductCategory, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, editable=False)
    description = models.TextField()
    features = models.TextField(blank=True, null=True, help_text="Enter features as bullet points, one per line")
    specifications = models.TextField(blank=True, null=True, help_text="Enter specs as key:value pairs, one per line")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['category', 'order']


class Page(models.Model):
    """Static pages like About Us, Contact, etc."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, editable=False)
    content = models.TextField()
    meta_description = models.TextField(blank=True, null=True, help_text="SEO meta description")
    featured_image = models.ImageField(upload_to='pages/', blank=True, null=True)
    active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """Customer testimonials"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    quote = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Testimonial from {self.name}"
    
    class Meta:
        ordering = ['order']


class ContactInquiry(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Inquiry from {self.name}: {self.subject}"
    
    class Meta:
        verbose_name_plural = "Contact Inquiries"
        ordering = ['-date_submitted']
