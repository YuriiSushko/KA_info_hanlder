from django.contrib import admin
from data_tracker.courses.models import Course, Status, Item, ActionLog, Video, BugType, BugReport
from data_tracker.users.models import Mortals, Roles
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from data_tracker.courses.forms import BugReportAdminForm, BugReportInlineForm
from django.urls import reverse
from django.contrib.contenttypes.admin import GenericTabularInline
from data_tracker.courses.filters import *

# class BugReportInline(GenericTabularInline):
#     model = BugReport
#     form = BugReportInlineForm
#     extra = 0
#     ct_field = "content_type"
#     ct_fk_field = "object_id"

#     def get_formset(self, request, obj=None, **kwargs):
#         formset = super().get_formset(request, obj, **kwargs)

#         class PrefilledFormSet(formset):
#             def _construct_form(self, i, **kwargs):
#                 form = super()._construct_form(i, **kwargs)
#                 form._parent_obj = obj
#                 return form

#         return PrefilledFormSet

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'get_courses', 'status', 'get_link', 'get_link_ka', 'last_modified')
    list_filter = ('type', ItemStatusFilter, ItemAuditorFilter, UaMathCourseFilter, KaMathCourseFilter, UaScienceCourseFilter, KaScienceCourseFilter)
    search_fields = ['title']
    readonly_fields = ('last_modified','updated_by','title', 'type', 'courses','number_of_words')
    # inlines = [BugReportInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('status', 'auditor', 'translator', 'updated_by').prefetch_related('courses')

    def save_model(self, request, obj, form, change):
        """
        This method is used to track which user made the last update.
        """
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
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
        elif db_field.name == 'status':
            all_statuses = list(Status.objects.all())
            pks = [s.pk for s in all_statuses if not s.video_related_status]
            kwargs['queryset'] = Status.objects.filter(pk__in=pks)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'type', 'get_object_link', 'who', 'get_local_time', 'new_status', 'comment')
    list_display_links = None
    date_hierarchy = 'date'
    search_fields = ['title', 'type', 'comment']
    list_filter = ('action', 'type', 'new_status', WhoPerformedFilter)

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
    get_local_time.short_description = 'Last modified'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class StatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'comments', 'video_related_status', 'platform_related_status', 'youtube_related_status')
    list_editable = ['video_related_status', 'platform_related_status', 'youtube_related_status']
    search_fields = ['title']
    list_filter = ('title',)

class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    list_display = ('title', 'description', 'course_type', 'created_at')
    search_fields = ['title']
    list_filter = ('created_at','course_type')

class VideoAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'get_courses', 'combined_status_display', 'get_links', 'translation_issue', 'last_modified')
    list_editable = ['translation_issue']
    list_display_links = ['title'] 
    list_filter = (VideoStatusFilter, YoutubeStatusFilter, PlatformStatusFilter, 'translation_issue', VideoAuditorFilter, UaMathCourseFilter, KaMathCourseFilter, UaScienceCourseFilter, KaScienceCourseFilter)
    search_fields = ['title']
    readonly_fields = ('last_modified','updated_by','type','courses','title','duration')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('video_status')
        qs = qs.prefetch_related('platform_status', 'youtube_status', 'courses')
        return qs

    def save_model(self, request, obj, form, change):
        """
        This method is used to track which user made the last update.
        """
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def combined_status_display(self, obj):
        statuses = [
            obj.video_status.title if obj.video_status else None,
            obj.platform_status.title if obj.platform_status else None,
            obj.youtube_status.title if obj.youtube_status else None,
        ]
        return ", ".join(filter(None, statuses)) or "—"
    combined_status_display.short_description = "Statuses"

    def get_links(self, obj):
        links = []
        
        if obj.portal_link:
            links.append(format_html('<a href="{}" target="_blank" rel="noopener noreferrer">TP Link</a>', obj.portal_link))
        if obj.translated_yt_link:
            links.append(format_html('<a href="{}" target="_blank" rel="noopener noreferrer">Translated YT</a>', obj.translated_yt_link))
        if obj.yt_link:
            links.append(format_html('<a href="{}" target="_blank" rel="noopener noreferrer">Original YT</a>', obj.yt_link))
        if obj.localized_link:
            links.append(format_html('<a href="{}" target="_blank" rel="noopener noreferrer">Khan Academy</a>', obj.localized_link))
        return format_html(" | ".join(links)) if links else "—"
    get_links.short_description = 'Links'    
    
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
        elif db_field.name == 'video_status':
            all_statuses = list(Status.objects.all())
            pks = [s.pk for s in all_statuses if s.video_related_status and not s.platform_related_status and not s.youtube_related_status]
            kwargs['queryset'] = Status.objects.filter(pk__in=pks)
        elif db_field.name == 'platform_status':
            all_statuses = list(Status.objects.all())
            pks = [s.pk for s in all_statuses if s.video_related_status and s.platform_related_status]
            kwargs['queryset'] = Status.objects.filter(pk__in=pks)
        elif db_field.name == 'youtube_status':
            all_statuses = list(Status.objects.all())
            pks = [s.pk for s in all_statuses if s.video_related_status and s.youtube_related_status]
            kwargs['queryset'] = Status.objects.filter(pk__in=pks)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_courses(self, obj):
        """
        Fetch the list of courses that this item belongs to.
        This will return a comma-separated list of course titles.
        """
        courses = obj.courses.all()
        return ", ".join(course.title for course in courses) if courses else "None"
    get_courses.short_description = 'Courses'

class BugReportAdmin(admin.ModelAdmin):
    form = BugReportAdminForm
    list_display = ('title', 'related_object_title', 'content_type_label', 'bug_type', 'assigned_to', 'is_resolved', 'reported_by', 'added_by', 'created_at')
    list_filter = (FilteredContentTypeListFilter, FilteredAssignedToListFilter, FilteredReportedByListFilter, 'is_resolved')
    list_editable = ['is_resolved']
    search_fields = ['title']
    
    def content_type_label(self, obj):
        ct = obj.content_type.model
        if ct == 'video':
            return 'Video'
        elif ct == 'item':
            if hasattr(obj.content_object, 'type'):
                if obj.content_object.type == 'article':
                    return 'Article'
                elif obj.content_object.type == 'exercise':
                    return 'Exercise'
            return 'Item'
        return ct.capitalize()
    content_type_label.short_description = 'Content Type'
    
    def related_object_title(self, obj):
        try:
            content_object = obj.content_object
            if not content_object:
                return f"[Missing Object ID {obj.object_id}]"

            ct = obj.content_type
            admin_url = reverse(f"admin:{ct.app_label}_{ct.model}_change", args=[obj.object_id])
            return format_html('<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>', admin_url, str(content_object))
        except Exception:
            return f"[Broken Link ID {obj.object_id}]"

    related_object_title.short_description = 'Content Title'
    
    def save_model(self, request, obj, form, change):
        if obj.added_by is None:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('bug_type', 'content_type', 'assigned_to')


admin.site.register(Course, CourseAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ActionLog, ActionLogAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(BugReport, BugReportAdmin)
admin.site.register(BugType)
