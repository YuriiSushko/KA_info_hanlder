from django.contrib import admin
from data_tracker.courses.models import Course, Status, Item, ActionLog, Video
from data_tracker.users.models import Mortals, Roles
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter

class CourseFilter(SimpleListFilter):
    title = ('Course')
    parameter_name = 'course'

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
            return queryset.filter(courses__id=self.value())
        return queryset

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'get_courses', 'status', 'get_link', 'get_link_ka', 'last_modified')
    list_filter = ('type', 'status', CourseFilter)
    search_fields = ['title']
    readonly_fields = ('last_modified','updated_by','title', 'type', 'courses','number_of_words')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('status', 'auditor', 'translator', 'updated_by').prefetch_related('courses')

    def save_model(self, request, obj, form, change):
        """
        This method is used to track which user made the last update.
        """
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    # def get_auditor(self, obj):
    #     """
    #     Fetch the specific 'Auditor' for the item.
    #     This will return only the user assigned as the auditor for the given item.
    #     """
    #     if obj.auditor:
    #         return f"{obj.auditor.first_name} {obj.auditor.last_name}"
    #     return "None"
    # get_auditor.short_description = 'Auditor'

    # def get_translator(self, obj):
    #     """
    #     Fetch the specific 'Translator' for the item.
    #     This will return only the user assigned as the translator for the given item.
    #     """
    #     if obj.translator:
    #         return f"{obj.translator.first_name} {obj.translator.last_name}"
    #     return "None"
    # get_translator.short_description = 'Translator'
    
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
            return format_html('<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>', obj.link, "TP Link")
    get_link.short_description = 'Translation portal'

    def get_link_ka(self, obj):
        if obj.external_link:
            return format_html('<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>', obj.external_link, "KA Link")
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
    list_display = ('action', 'type', 'get_object_link', 'who', 'get_local_time', 'new_status', 'comment')
    list_display_links = None
    date_hierarchy = 'date'
    search_fields = ['title', 'type', 'comment']
    list_filter = ('action', 'type', 'new_status')

    def get_object_link(self, obj):
        if hasattr(obj, 'item') and obj.item_id:
            obj_name, obj_id, changepath = obj.item.title, obj.item_id, 'item'
        elif hasattr(obj, 'video') and obj.video_id:
            obj_name, obj_id, changepath = obj.video.title, obj.video_id, 'video'
        else:
            return '-'

        url = f"/admin/courses/{changepath}/{obj_id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj_name)
    get_object_link.short_description = 'Object'

    def get_local_time(self, obj):
        return obj.date.strftime('%Y-%m-%d %H:%M:%S')
    get_local_time.short_description = 'Local Time'

    # readonly_fields = ('action', 'type', 'item', 'who', 'new_status', 'date', 'comment')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class StatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'comments', 'video_related_status')
    list_editable = ['video_related_status']
    search_fields = ['title']
    list_filter = ('title',)

class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    list_display = ('title', 'description', 'created_at')
    search_fields = ['title']
    list_filter = ('created_at',)
    
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_courses', 'video_status', 'get_link', 'get_link_yt', 'platform_status', 'youtube_status', 'translation_issue', 'last_modified')
    list_editable = ['translation_issue']
    list_filter = ('video_status', 'platform_status', 'youtube_status', 'translation_issue', CourseFilter)
    search_fields = ['title']
    readonly_fields = ('last_modified','updated_by','type','courses','title','duration')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('video_status', 'platform_status', 'youtube_status', 'auditor', 'actor', 'updated_by').prefetch_related('courses')

    def save_model(self, request, obj, form, change):
        """
        This method is used to track which user made the last update.
        """
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def get_link(self, obj):
        if obj.portal_link:
            return format_html('<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>', obj.portal_link, "TP Link")
    get_link.short_description = 'Translation portal'

    def get_link_yt(self, obj):
        if obj.translated_yt_link:
            return format_html('<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>', obj.translated_yt_link, "KA Link")
    get_link_yt.short_description = 'Translated yt'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        This method is used to filter the available options in the foreign key field
        to only show users with the "Auditor" or "Translator" role when selecting an Auditor or Translator.
        """
        if db_field.name == "auditor":
            auditor_role = Roles.objects.get(title="Auditor")
            kwargs["queryset"] = Mortals.objects.filter(groups=auditor_role)
        elif db_field.name == "actor":
            actor_role = Roles.objects.get(title="Actor")
            kwargs["queryset"] = Mortals.objects.filter(groups=actor_role)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_courses(self, obj):
        """
        Fetch the list of courses that this item belongs to.
        This will return a comma-separated list of course titles.
        """
        courses = obj.courses.all()
        return ", ".join(course.title for course in courses) if courses else "None"
    get_courses.short_description = 'Courses'

admin.site.register(Course, CourseAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ActionLog, ActionLogAdmin)
admin.site.register(Video, VideoAdmin)
