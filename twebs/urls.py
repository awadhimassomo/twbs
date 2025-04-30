"""
URL configuration for twebs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminpage/', include('adminpage.urls')),  # Custom admin interface
    path('', include('website.urls')),
]

# Add URL pattern for directly serving static files
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add URL patterns for style.css and other static files
urlpatterns += [
    path('static/<path:path>', serve, {
        'document_root': os.path.join(base_dir, 'website/static'),
    }),
    path('style.css', serve, {
        'document_root': os.path.join(base_dir, 'website/static/website/css'),
        'path': 'style.css',
    }),
    path('media/<path:path>', serve, {
        'document_root': os.path.join(base_dir, 'media'),
    }),
]

# Add static URL patterns in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static('/media/', document_root=os.path.join(base_dir, 'media'))
