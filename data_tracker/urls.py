"""
URL configuration for data_tracker project.

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
from django.urls import path, include
from django.http import HttpResponse
from data_tracker.admin_site import custom_admin_site

# Add a view for the root URL
def home(request):
    return HttpResponse("Welcome to the Home Page! Add admin/ to url to go to the admin panel")  # Replace with a template or other content

# Define a view for the favicon.ico request
def favicon(request):
    return HttpResponse(status=204)  # Return empty response for favicon

urlpatterns = [
    path('favicon.ico', favicon),  # Handle favicon.ico requests
    path('', home),  # Root URL points to the custom home view'
    # path('admin/', admin.site.urls),
    path('admin/', custom_admin_site.urls),  # Admin URL remains the same
]

