from django.contrib import admin
from data_tracker.courses.models import Course, Status, Item, ActionLog, Video, BugType, BugReport
from data_tracker.users.models import Mortals, Roles
from data_tracker.crm.models import User
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from data_tracker.courses.forms import BugReportAdminForm
from django.urls import reverse


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
    
class VideoAuditorFilter(admin.SimpleListFilter):
    title = 'auditor'
    parameter_name = 'auditor'
    
    def lookups(self, request, model_admin):
        try:
            users = Video.objects.exclude(auditor__isnull=True).values_list('auditor', flat=True).distinct()
            results = [(user.pk, str(user)) for user in Mortals.objects.filter(pk__in=users)]
            results.append(('__none__', 'None'))
            return results
        except Roles.DoesNotExist:
            return [('__none__', 'None')]

    def queryset(self, request, queryset):
        value = self.value()
        if value == '__none__':
            return queryset.filter(auditor__isnull=True)
        elif value:
            return queryset.filter(auditor__pk=value)
        return queryset
    
class ItemAuditorFilter(admin.SimpleListFilter):
    title = 'auditor'
    parameter_name = 'auditor'
    
    def lookups(self, request, model_admin):
        try:
            users = Item.objects.exclude(auditor__isnull=True).values_list('auditor', flat=True).distinct()
            results = [(user.pk, str(user)) for user in Mortals.objects.filter(pk__in=users)]
            results.append(('__none__', 'None'))
            return results
        except Roles.DoesNotExist:
            return [('__none__', 'None')]

    def queryset(self, request, queryset):
        value = self.value()
        if value == '__none__':
            return queryset.filter(auditor__isnull=True)
        elif value:
            return queryset.filter(auditor__pk=value)
        return queryset

class ItemStatusFilter(admin.SimpleListFilter):
    title = ('Item Status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        all_statuses = list(Status.objects.all())
        choices = [
            (s.pk, s.title) 
            for s in all_statuses 
            if not s.video_related_status
        ]
        return choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__pk=self.value())
        return queryset

class UaMathCourseFilter(admin.SimpleListFilter):
    title = ('math(Ukraine)')
    parameter_name = 'math_ukraine'

    def lookups(self, request, model_admin):
        courses = Course.objects.all()
        return [(course.id, course.title) for course in courses.filter(course_type='math(ukraine)')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(courses__id=self.value())
        return queryset
    
class KaMathCourseFilter(admin.SimpleListFilter):
    title = ('math(Khan Academy)')
    parameter_name = 'math_khan_academy'

    def lookups(self, request, model_admin):
        courses = Course.objects.all()
        return [(course.id, course.title) for course in courses.filter(course_type='math(khan academy)')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(courses__id=self.value())
        return queryset

class UaScienceCourseFilter(admin.SimpleListFilter):
    title = ('science(Ukraine)')
    parameter_name = 'science_ukraine'

    def lookups(self, request, model_admin):
        courses = Course.objects.all()
        return [(course.id, course.title) for course in courses.filter(course_type='science(ukraine)')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(courses__id=self.value())
        return queryset
    
class KaScienceCourseFilter(admin.SimpleListFilter):
    title = ('science(Khan Academy)')
    parameter_name = 'science_khan_academy'

    def lookups(self, request, model_admin):
        courses = Course.objects.all()
        return [(course.id, course.title) for course in courses.filter(course_type='science(khan academy)')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(courses__id=self.value())
        return queryset
    
class WhoPerformedFilter(admin.SimpleListFilter):
    title = 'Who performed'
    parameter_name = 'who'

    def lookups(self, request, model_admin):
        user_ids = ActionLog.objects.filter(who__isnull=False).values_list('who_id', flat=True).distinct()
        users = Mortals.objects.filter(id__in=user_ids)
        return [(user.id, f"{user.first_name} {user.last_name}") for user in users]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(who_id=self.value())
        return queryset
    
class VideoStatusFilter(admin.SimpleListFilter):
    title = ('Video Status')
    parameter_name = 'video_status'

    def lookups(self, request, model_admin):
        try:
            all_statuses = list(Status.objects.all())
            choices = [
                (s.pk, s.title) 
                for s in all_statuses 
                if s.video_related_status and not s.platform_related_status and not s.youtube_related_status
            ]
            choices.append(('__none__', 'None'))
            return choices
        except Status.DoesNotExist:
            return [('__none__', 'None')]

    def queryset(self, request, queryset):
        value = self.value()
        if value == '__none__':
            return queryset.filter(video_status__isnull=True)
        elif value:
            return queryset.filter(video_status__pk=value)
        return queryset
    
class PlatformStatusFilter(admin.SimpleListFilter):
    title = ('Platform Status')
    parameter_name = 'platform_status'

    def lookups(self, request, model_admin):
        try:
            all_statuses = list(Status.objects.all())
            choices = [
                (s.pk, s.title) 
                for s in all_statuses 
                if s.video_related_status and s.platform_related_status
            ]
            choices.append(('__none__', 'None'))
            return choices
        except Status.DoesNotExist:
            return [('__none__', 'None')]

    def queryset(self, request, queryset):
        value = self.value()
        if value == '__none__':
            return queryset.filter(platfrom_status__isnull=True)
        elif value:
            return queryset.filter(platform_status__pk=value)
        return queryset

class YoutubeStatusFilter(admin.SimpleListFilter):
    title = ('Video Status')
    parameter_name = 'video_status'

    def lookups(self, request, model_admin):
        try:
            all_statuses = list(Status.objects.all())
            choices = [
                (s.pk, s.title) 
                for s in all_statuses 
                if s.video_related_status and s.youtube_related_status
            ]
            choices.append(('__none__', 'None'))
            return choices
        except Status.DoesNotExist:
            return [('__none__', 'None')]

    def queryset(self, request, queryset):
        value = self.value()
        if value == '__none__':
            return queryset.filter(youtube_status__isnull=True)
        elif value:
            return queryset.filter(youtube_status__pk=value)
        return queryset
    
class FilteredContentTypeListFilter(SimpleListFilter):
    title = 'Content Type'
    parameter_name = 'content_type'

    def lookups(self, request, model_admin):
        return [
            ('video', 'Video'),
            ('article', 'Article'),
            ('exercise', 'Exercise'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'video':
            ct = ContentType.objects.get(model='video')
            return queryset.filter(content_type=ct)
        elif value in ['article', 'exercise']:
            ct = ContentType.objects.get(model='item')
            return queryset.filter(content_type=ct, object_id__in=Item.objects.filter(type=value).values_list('pk'))
        return queryset
    
class FilteredReportedByListFilter(SimpleListFilter):
    title = 'Reported By'
    parameter_name = 'reported_by'

    def lookups(self, request, model_admin):
        options = []

        for model in [Mortals, User]:
            ct = ContentType.objects.get_for_model(model)
            ids = BugReport.objects.filter(
                reported_by_content_type=ct
            ).values_list('reported_by_object_id', flat=True).distinct()
            instances = model.objects.filter(pk__in=ids)
            options += [(f"{ct.pk}-{i.pk}", f"{i}") for i in instances]

        return options

    def queryset(self, request, queryset):
        val = self.value()
        if val:
            try:
                ct_pk, obj_pk = map(int, val.split('-'))
                return queryset.filter(
                    reported_by_content_type_id=ct_pk,
                    reported_by_object_id=obj_pk
                )
            except (ValueError, TypeError):
                return queryset.none()
        return queryset

class FilteredAssignedToListFilter(SimpleListFilter):
    title = 'Assigned To'
    parameter_name = 'assigned_to'

    def lookups(self, request, model_admin):
        users = BugReport.objects.exclude(assigned_to__isnull=True).values_list('assigned_to', flat=True).distinct()
        return [(user.pk, str(user)) for user in Mortals.objects.filter(pk__in=users)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(assigned_to__id=self.value())
        return queryset