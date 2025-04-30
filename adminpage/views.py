from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse

from website.models import (
    SiteSettings, 
    ProductCategory, 
    Product, 
    Testimonial, 
    ContactInquiry
)
from .forms import (
    LoginForm,
    SignupForm,
    SiteSettingsForm,
    ProductCategoryForm,
    ProductForm,
    TestimonialForm
)

# Authentication Views
def admin_login(request):
    """Login view for admin users"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('adminpage:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('adminpage:dashboard')
            else:
                messages.error(request, 'Invalid login credentials or insufficient permissions.')
    else:
        form = LoginForm()
    
    return render(request, 'adminpage/login.html', {'form': form})

def admin_signup(request):
    """Registration view for new admin users"""
    if request.user.is_authenticated:
        return redirect('adminpage:dashboard')
        
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Automatically log in the new user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}. You are now logged in.')
            return redirect('adminpage:dashboard')
    else:
        form = SignupForm()
    
    return render(request, 'adminpage/signup.html', {'form': form})

@login_required
def admin_logout(request):
    """Logout view for admin users"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('adminpage:login')

# Dashboard
@login_required
def dashboard(request):
    """Admin dashboard showing overview of site content"""
    # Count various items for the dashboard
    products_count = Product.objects.count()
    categories_count = ProductCategory.objects.count()
    testimonials_count = Testimonial.objects.count()
    inquiries_count = ContactInquiry.objects.count()
    unread_inquiries = ContactInquiry.objects.filter(is_read=False).count()
    
    # Latest inquiries for quick access
    latest_inquiries = ContactInquiry.objects.order_by('-date_submitted')[:5]
    
    context = {
        'products_count': products_count,
        'categories_count': categories_count,
        'testimonials_count': testimonials_count,
        'inquiries_count': inquiries_count,
        'unread_inquiries': unread_inquiries,
        'latest_inquiries': latest_inquiries,
    }
    
    return render(request, 'adminpage/dashboard.html', context)

# Site Settings
@login_required
def edit_settings(request):
    """Edit global site settings"""
    # Get or create site settings
    site_settings, created = SiteSettings.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=site_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site settings updated successfully.')
            return redirect('adminpage:settings')
    else:
        form = SiteSettingsForm(instance=site_settings)
    
    return render(request, 'adminpage/settings_form.html', {'form': form})

# Products Management
@login_required
def list_products(request):
    """List all products with pagination and filter options"""
    products = Product.objects.all().order_by('category', 'order')
    
    # Filter by category if specified
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Pagination
    paginator = Paginator(products, 10)  # 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for the filter dropdown
    categories = ProductCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'category_id': category_id,
        'search_query': search_query
    }
    
    return render(request, 'adminpage/products_list.html', context)

@login_required
def add_product(request):
    """Add a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('adminpage:products')
    else:
        form = ProductForm()
    
    return render(request, 'adminpage/product_form.html', {'form': form, 'title': 'Add Product'})

@login_required
def edit_product(request, pk):
    """Edit an existing product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('adminpage:products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'adminpage/product_form.html', {'form': form, 'title': 'Edit Product'})

@login_required
def delete_product(request, pk):
    """Delete a product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('adminpage:products')
    
    return render(request, 'adminpage/confirm_delete.html', {
        'object': product,
        'title': 'Delete Product',
        'cancel_url': 'adminpage:products'
    })

# Categories Management
@login_required
def list_categories(request):
    """List all product categories"""
    categories = ProductCategory.objects.all().order_by('order')
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        categories = categories.filter(name__icontains=search_query)
    
    # Pagination
    paginator = Paginator(categories, 10)  # 10 categories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query
    }
    
    return render(request, 'adminpage/categories_list.html', context)

@login_required
def add_category(request):
    """Add a new product category"""
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('adminpage:categories')
    else:
        form = ProductCategoryForm()
    
    return render(request, 'adminpage/category_form.html', {'form': form, 'title': 'Add Category'})

@login_required
def edit_category(request, pk):
    """Edit an existing product category"""
    category = get_object_or_404(ProductCategory, pk=pk)
    
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('adminpage:categories')
    else:
        form = ProductCategoryForm(instance=category)
    
    return render(request, 'adminpage/category_form.html', {'form': form, 'title': 'Edit Category'})

@login_required
def delete_category(request, pk):
    """Delete a product category"""
    category = get_object_or_404(ProductCategory, pk=pk)
    
    if request.method == 'POST':
        # Check if there are products in this category
        if category.products.exists():
            messages.error(request, 'Cannot delete category that contains products.')
            return redirect('adminpage:categories')
        
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('adminpage:categories')
    
    return render(request, 'adminpage/confirm_delete.html', {
        'object': category,
        'title': 'Delete Category',
        'cancel_url': 'adminpage:categories'
    })

# Testimonials Management
@login_required
def list_testimonials(request):
    """List all testimonials"""
    testimonials = Testimonial.objects.all().order_by('order')
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        testimonials = testimonials.filter(name__icontains=search_query)
    
    # Pagination
    paginator = Paginator(testimonials, 10)  # 10 testimonials per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query
    }
    
    return render(request, 'adminpage/testimonials_list.html', context)

@login_required
def add_testimonial(request):
    """Add a new testimonial"""
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial added successfully.')
            return redirect('adminpage:testimonials')
    else:
        form = TestimonialForm()
    
    return render(request, 'adminpage/testimonial_form.html', {'form': form, 'title': 'Add Testimonial'})

@login_required
def edit_testimonial(request, pk):
    """Edit an existing testimonial"""
    testimonial = get_object_or_404(Testimonial, pk=pk)
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial updated successfully.')
            return redirect('adminpage:testimonials')
    else:
        form = TestimonialForm(instance=testimonial)
    
    return render(request, 'adminpage/testimonial_form.html', {'form': form, 'title': 'Edit Testimonial'})

@login_required
def delete_testimonial(request, pk):
    """Delete a testimonial"""
    testimonial = get_object_or_404(Testimonial, pk=pk)
    
    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Testimonial deleted successfully.')
        return redirect('adminpage:testimonials')
    
    return render(request, 'adminpage/confirm_delete.html', {
        'object': testimonial,
        'title': 'Delete Testimonial',
        'cancel_url': 'adminpage:testimonials'
    })

# Contact Inquiries Management
@login_required
def list_inquiries(request):
    """List all contact inquiries"""
    inquiries = ContactInquiry.objects.all().order_by('-date_submitted')
    
    # Filter by read status if specified
    status = request.GET.get('status')
    if status == 'unread':
        inquiries = inquiries.filter(is_read=False)
    elif status == 'read':
        inquiries = inquiries.filter(is_read=True)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        inquiries = inquiries.filter(name__icontains=search_query) | \
                   inquiries.filter(email__icontains=search_query) | \
                   inquiries.filter(subject__icontains=search_query)
    
    # Pagination
    paginator = Paginator(inquiries, 10)  # 10 inquiries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status': status,
        'search_query': search_query
    }
    
    return render(request, 'adminpage/inquiries_list.html', context)

@login_required
def view_inquiry(request, pk):
    """View a specific contact inquiry"""
    inquiry = get_object_or_404(ContactInquiry, pk=pk)
    
    # Mark as read if it's not already
    if not inquiry.is_read:
        inquiry.is_read = True
        inquiry.save()
    
    return render(request, 'adminpage/inquiry_detail.html', {'inquiry': inquiry})

@login_required
def mark_inquiry_read(request, pk):
    """Mark an inquiry as read or unread"""
    inquiry = get_object_or_404(ContactInquiry, pk=pk)
    
    # Toggle read status
    inquiry.is_read = not inquiry.is_read
    inquiry.save()
    
    if request.is_ajax():
        return JsonResponse({'status': 'success', 'is_read': inquiry.is_read})
    
    messages.success(request, f'Inquiry marked as {"read" if inquiry.is_read else "unread"}.')
    return redirect('adminpage:inquiries')

@login_required
def delete_inquiry(request, pk):
    """Delete a contact inquiry"""
    inquiry = get_object_or_404(ContactInquiry, pk=pk)
    
    if request.method == 'POST':
        inquiry.delete()
        messages.success(request, 'Inquiry deleted successfully.')
        return redirect('adminpage:inquiries')
    
    return render(request, 'adminpage/confirm_delete.html', {
        'object': inquiry,
        'title': 'Delete Inquiry',
        'cancel_url': 'adminpage:inquiries'
    })
