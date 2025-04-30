from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
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

def get_common_context():
    """Get common context data for all views"""
    context = {}
    
    # Get site settings
    try:
        context['site_settings'] = SiteSettings.objects.first()
    except:
        context['site_settings'] = None
    
    # Get product categories for navbar
    try:
        context['product_categories'] = ProductCategory.objects.all()
    except:
        context['product_categories'] = []
        
    # Add static product categories if none in database
    if not context['product_categories']:
        context['product_categories'] = [
            {'name': 'Air Filter Systems', 'slug': 'air-filter-systems'},
            {'name': 'Mask Evaluation Systems', 'slug': 'mask-evaluation-systems'},
            {'name': 'Dust Sensor Systems', 'slug': 'dust-sensor-systems'},
            {'name': 'Generators', 'slug': 'generators'},
            {'name': 'Air Quality Monitoring', 'slug': 'air-quality-monitoring'},
        ]
    
    # Add application categories
    context['applications_enabled'] = True
    context['application_categories'] = [
        {'name': 'Materials Testing', 'url': '#'},
        {'name': 'Microscopy', 'url': '#'},
        {'name': 'Spectroscopy', 'url': '#'},
    ]
    
    # Add other context items as needed
    
    return context


def home(request):
    """View for the homepage"""
    context = get_common_context()
    
    # Get homepage sections
    hero_section = HomePageSection.objects.filter(section_type='hero', active=True).first()
    services_section = HomePageSection.objects.filter(section_type='services', active=True).first()
    why_us_section = HomePageSection.objects.filter(section_type='why_us', active=True).first()
    
    # Get service cards
    service_cards = ServiceCard.objects.filter(active=True)
    
    # Get testimonials
    testimonials = Testimonial.objects.filter(active=True)
    
    context.update({
        'hero_section': hero_section,
        'services_section': services_section,
        'why_us_section': why_us_section,
        'service_cards': service_cards,
        'testimonials': testimonials,
    })
    
    return render(request, 'website/index.html', context)


def products(request, category_slug=None):
    """View for the products page"""
    context = get_common_context()
    
    if category_slug:
        # Show products for a specific category
        category = get_object_or_404(ProductCategory, slug=category_slug)
        products_list = Product.objects.filter(category=category, active=True)
        context['category'] = category
    else:
        # Show all products
        products_list = Product.objects.filter(active=True)
    
    context['products'] = products_list
    
    return render(request, 'website/products.html', context)


def product_detail(request, product_slug):
    """View for individual product details"""
    context = get_common_context()
    
    product = get_object_or_404(Product, slug=product_slug, active=True)
    
    # Process features and specifications
    if product.features:
        features = [f.strip() for f in product.features.split('\n') if f.strip()]
    else:
        features = []
        
    if product.specifications:
        specs = {}
        for line in product.specifications.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                specs[key.strip()] = value.strip()
    else:
        specs = {}
    
    context.update({
        'product': product,
        'features': features,
        'specifications': specs,
    })
    
    return render(request, 'website/product_detail.html', context)


def page_view(request, slug):
    """View for static pages like About Us, etc."""
    context = get_common_context()
    
    page = get_object_or_404(Page, slug=slug, active=True)
    context['page'] = page
    
    return render(request, 'website/page.html', context)


def custom_page(request, page_slug):
    """View for custom pages from the database"""
    context = get_common_context()
    
    page = get_object_or_404(Page, slug=page_slug, active=True)
    context['page'] = page
    
    return render(request, 'website/page.html', context)


def about(request):
    """View for the about page"""
    # Try to get About page from database
    try:
        page = Page.objects.get(slug='about', active=True)
        return page_view(request, 'about')
    except Page.DoesNotExist:
        # Fallback to template if no database entry
        context = get_common_context()
        return render(request, 'website/about.html', context)


def contact(request):
    """View for the contact page"""
    context = get_common_context()
    
    if request.method == 'POST':
        # Process contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            # Save the inquiry to database
            ContactInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            messages.success(request, "Thank you for your message. We'll get back to you shortly.")
            return redirect('website:contact')
        else:
            messages.error(request, "Please fill in all required fields.")
    
    # Try to get Contact page from database
    try:
        page = Page.objects.get(slug='contact', active=True)
        context['page'] = page
    except Page.DoesNotExist:
        # No custom page content
        pass
    
    return render(request, 'website/contact.html', context)
