from django.contrib import admin
from data_tracker.users.models import Mortals, Roles
from django.contrib.auth.models import Group
from data_tracker.users.forms import MortalsCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class MortalsAdmin(BaseUserAdmin):
    readonly_fields = ('last_seen',)
    add_form = MortalsCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'get_roles','last_seen')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

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