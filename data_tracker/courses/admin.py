from django.contrib import admin

# Customizing the admin interface for Course model
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')  # Fields to display in the list view
    search_fields = ('title', 'description')  # Add search functionality for these fields
    list_filter = ('created_at',)  # Filter courses by created date
    
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'object_type', 'object_id', 'people', 'date')  # Show key fields
    list_filter = ('action', 'object_type')  # Filter by action type and object type
    search_fields = ('object_type', 'people__name')  # Search by object type or people’s name

# Import models inside the register function to avoid circular imports
def get_models():
    from data_tracker.courses.models import Course, Item, ActionLog
    return Course, Item, ActionLog

# Register models with custom admin options
Course, Item, ActionLog = get_models()

admin.site.register(Course, CourseAdmin)
admin.site.register(Item)
admin.site.register(ActionLog, ActionLogAdmin)
