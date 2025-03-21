from django.contrib import admin
from data_tracker.courses.models import Course, Status, Item, ActionLog
from data_tracker.users.models import Mortals, Roles
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter

class CourseFilter(SimpleListFilter):
    title = ('Course')  # The filter title
    parameter_name = 'course'  # The parameter name used in the URL

    def lookups(self, request, model_admin):
        """
        Defines the options that will be shown in the filter dropdown.
        We will list all available courses.
        """
        courses = Course.objects.all()
        return [(course.id, course.title) for course in courses]

    def queryset(self, request, queryset):
        """
        Filters the queryset based on the selected course.
        """
        if self.value():
            return queryset.filter(courses__id=self.value())  # Filter items by course ID
        return queryset

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'get_courses', 'status', 'get_link', 'get_link_ka', 'get_auditor', 'get_translator', 'last_modified')
    list_filter = ('type', 'status', CourseFilter)
    search_fields = ['title']

    def save_model(self, request, obj, form, change):
        """
        This method is used to track which user made the last update.
        """
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def get_auditor(self, obj):
        """
        Fetch the specific 'Auditor' for the item.
        This will return only the user assigned as the auditor for the given item.
        """
        if obj.auditor:
            return f"{obj.auditor.first_name} {obj.auditor.last_name}"
        return "None"
    get_auditor.short_description = 'Auditor'

    def get_translator(self, obj):
        """
        Fetch the specific 'Translator' for the item.
        This will return only the user assigned as the translator for the given item.
        """
        if obj.translator:
            return f"{obj.translator.first_name} {obj.translator.last_name}"
        return "None"
    get_translator.short_description = 'Translator'
    
    def get_courses(self, obj):
        """
        Fetch the list of courses that this item belongs to.
        This will return a comma-separated list of course titles.
        """
        courses = obj.courses.all()
        return ", ".join(course.title for course in courses) if courses else "None"
    get_courses.short_description = 'Courses'
    
    def get_link(self, obj):
        if obj.link:
            return format_html('<a href="{}">{}</a>', obj.link, "TP Link")
    get_link.short_description = 'Translation portal'
    
    def get_link_ka(self, obj):
        if obj.external_link:
             return format_html('<a href="{}">{}</a>', obj.external_link, "KA Link")
    get_link_ka.short_description = 'Khan Academy'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        This method is used to filter the available options in the foreign key field
        to only show users with the "Auditor" or "Translator" role when selecting an Auditor or Translator.
        """
        if db_field.name == "auditor":
            auditor_role = Roles.objects.get(title="Auditor")
            kwargs["queryset"] = Mortals.objects.filter(groups=auditor_role)
        elif db_field.name == "translator":
            translator_role = Roles.objects.get(title="Translator")
            kwargs["queryset"] = Mortals.objects.filter(groups=translator_role)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'type', 'get_item_link', 'who', 'get_local_time', 'new_status', 'comment')
    search_fields = ['item_title', 'type', 'comment']
    list_filter = ('action', 'type', 'new_status')

    def get_item_link(self, obj):
        return format_html('<a href="/admin/courses/item/{}/change/">{}</a>', obj.item.id, obj.item.title)
    get_item_link.short_description = 'Item Link'

    def get_local_time(self, obj):
        return obj.date.strftime('%Y-%m-%d %H:%M:%S')
    get_local_time.short_description = 'Local Time'

    readonly_fields = ('action', 'type', 'item', 'who', 'new_status', 'date', 'comment')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class StatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'comments')
    search_fields = ['title']
    list_filter = ('title',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')
    search_fields = ['title']
    list_filter = ('created_at',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ActionLog, ActionLogAdmin)
