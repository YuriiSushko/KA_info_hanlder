from django.contrib import admin
from data_tracker.courses.models import Course, Status, Item, ActionLog
from data_tracker.users.models import Mortals, Roles
from django.utils.html import format_html

# # People Admin
# class PeopleAdmin(admin.ModelAdmin):
#     list_display = ('name', 'surname', 'get_roles')
#     search_fields = ('name', 'surname', 'roles__title')
#     list_filter = ('roles',)

#     def get_roles(self, obj):
#         return ", ".join(role.title for role in obj.roles.all())
#     get_roles.short_description = 'Roles'

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'status', 'get_auditor', 'get_translator', 'last_modified')
    list_filter = ('type', 'status')
    search_fields = ('title')

    def save_model(self, request, obj, form, change):
        """
        This method is used to track which user made the last update.
        """
        obj.updated_by = request.user  # Track the user who made the change
        super().save_model(request, obj, form, change)

    def get_auditor(self, obj):
        # Fetch the 'Auditor' role
        auditor_role = Roles.objects.get(title="Auditor")  # Assuming you have a role called 'Auditor'
        
        # Find the user (Mortals) who has this role
        auditor = Mortals.objects.filter(groups=auditor_role).first()  # Gets the first auditor user
        
        return f"{auditor.first_name} {auditor.last_name}" if auditor else ''
    get_auditor.short_description = 'Auditor'

    def get_translator(self, obj):
        # Fetch the 'Translator' role
        translator_role = Roles.objects.get(title="Translator")  # Assuming you have a role called 'Translator'
        
        # Find the user (Mortals) who has this role
        translator = Mortals.objects.filter(groups=translator_role).first()  # Gets the first translator user
        
        return f"{translator.first_name} {translator.last_name}" if translator else ''
    get_translator.short_description = 'Translator'



class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'type', 'item', 'who', 'get_local_time', 'new_status', 'comment')
    search_fields = ('item_title')
    list_filter = ('action', 'type', 'new_status')

    def get_item_link(self, obj):
        # Use format_html to ensure the link is rendered as HTML
        return format_html('<a href="/admin/courses/item/{}/change/">{}</a>', obj.item.id, obj.item.title)
    get_item_link.short_description = 'Item Link'

    def get_local_time(self, obj):
        return obj.date.strftime('%Y-%m-%d %H:%M:%S')  # Adjust to your preferred format
    get_local_time.short_description = 'Local Time'

    readonly_fields = ('action', 'type', 'item', 'who', 'new_status', 'date', 'comment')

    def has_add_permission(self, request, obj=None):
        return False  # Prevent adding new ActionLog entries

    def has_change_permission(self, request, obj=None):
        return False  # Prevent modifying ActionLog entries

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deleting ActionLog entries

# Status Admin
class StatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'comments')  # Display title and comments
    search_fields = ('title',)  # Enable search by title
    list_filter = ('title',)  # Add filter for title

# # Role Admin
# class RoleAdmin(admin.ModelAdmin):
#     list_display = ('title',)  # Display role title
#     search_fields = ('title',)  # Enable search by title
#     list_filter = ('title',)  # Add filter for title

# Course Admin
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')  # Display title, description, and created_at
    search_fields = ('title', 'description')  # Enable search by title and description
    list_filter = ('created_at',)  # Add filter for created_at date

# Register models in the admin site
admin.site.register(Course, CourseAdmin)  # Register custom CourseAdmin
admin.site.register(Status, StatusAdmin)  # Register custom StatusAdmin
admin.site.register(Item, ItemAdmin)
admin.site.register(ActionLog, ActionLogAdmin)
