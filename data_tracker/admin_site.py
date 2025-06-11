from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from data_tracker.users.models import Mortals
from django.contrib.admin.sites import AlreadyRegistered, AdminSite

class CustomAdminSite(AdminSite):
    site_header = 'Адмінка'

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        if not request.user.groups.filter(name='crm admin').exists():
            app_list = [app for app in app_list if app['app_label'] != 'crm']
        return app_list
    
    def index(self, request, extra_context=None):
        online_threshold = timezone.now() - timedelta(minutes=10)
        online_users = Mortals.objects.filter(last_seen__gte=online_threshold)
        
        extra_context = extra_context or {}
        extra_context['online_users'] = online_users
        
        return super().index(request, extra_context=extra_context)

custom_admin_site = CustomAdminSite(name='custom_admin')

for model, model_admin in admin.site._registry.items():
    try:
        custom_admin_site.register(model, model_admin.__class__)
    except AlreadyRegistered:
        pass
