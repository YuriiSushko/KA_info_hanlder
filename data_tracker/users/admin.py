from django.contrib import admin
from data_tracker.users.models import Mortals, Roles
from django.contrib.auth.models import Group

class MortalsAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'get_roles')

    def get_roles(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_roles.short_description = 'Roles'
    
class RolesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

admin.site.register(Mortals, MortalsAdmin)
admin.site.register(Roles, RolesAdmin)

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass