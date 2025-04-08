from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered, AdminSite

class CustomAdminSite(AdminSite):
    site_header = 'Custom Administration'

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        if not request.user.groups.filter(name='crm admin').exists():
            app_list = [app for app in app_list if app['app_label'] != 'crm']
        return app_list

custom_admin_site = CustomAdminSite(name='custom_admin')

for model, model_admin in admin.site._registry.items():
    try:
        custom_admin_site.register(model, model_admin.__class__)
    except AlreadyRegistered:
        pass
