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
    search_fields = ['title']

    def save_model(self, request, obj, form, change):
        """
        This method is used to track which user made the last update.
        """
        obj.updated_by = request.user  # Track the user who made the change
        super().save_model(request, obj, form, change)

    def get_auditor(self, obj):
        """
        Fetch the specific 'Auditor' for the item.
        This will return only the user assigned as the auditor for the given item.
        """
        if obj.auditor:
            return f"{obj.auditor.first_name} {obj.auditor.last_name}"
        return "None"  # Return a default value if no auditor is assigned
    get_auditor.short_description = 'Auditor'

    def get_translator(self, obj):
        """
        Fetch the specific 'Translator' for the item.
        This will return only the user assigned as the translator for the given item.
        """
        if obj.translator:
            return f"{obj.translator.first_name} {obj.translator.last_name}"
        return "None"  # Return a default value if no translator is assigned
    get_translator.short_description = 'Translator'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        This method is used to filter the available options in the foreign key field
        to only show users with the "Auditor" or "Translator" role when selecting an Auditor or Translator.
        """
        if db_field.name == "auditor":
            # Show all users with the "Auditor" role in the dropdown
            auditor_role = Roles.objects.get(title="Auditor")
            kwargs["queryset"] = Mortals.objects.filter(groups=auditor_role)
        elif db_field.name == "translator":
            # Show all users with the "Translator" role in the dropdown
            translator_role = Roles.objects.get(title="Translator")
            kwargs["queryset"] = Mortals.objects.filter(groups=translator_role)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'type', 'item', 'who', 'get_local_time', 'new_status', 'comment')
    search_fields = ['item_title', 'type', 'comment']
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
    search_fields = ['title']  # Enable search by title
    list_filter = ('title',)  # Add filter for title

# # Role Admin
# class RoleAdmin(admin.ModelAdmin):
#     list_display = ('title',)  # Display role title
#     search_fields = ('title',)  # Enable search by title
#     list_filter = ('title',)  # Add filter for title

# Course Admin
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')  # Display title, description, and created_at
    search_fields = ['title', 'description']  # Enable search by title and description
    list_filter = ('created_at',)  # Add filter for created_at date

# Register models in the admin site
admin.site.register(Course, CourseAdmin)  # Register custom CourseAdmin
admin.site.register(Status, StatusAdmin)  # Register custom StatusAdmin
admin.site.register(Item, ItemAdmin)
admin.site.register(ActionLog, ActionLogAdmin)
