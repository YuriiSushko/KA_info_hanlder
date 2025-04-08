from data_tracker.admin_site import custom_admin_site
from django.contrib import admin
from data_tracker.crm.models import User, Institution, SotialRole, KaRole, Event, EventType, EventParticipant
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.admin import SimpleListFilter

class SotialRoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ['title']

class KaRoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ['title']

class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ['title']

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'role')
    search_fields = ['name', 'email']
    
class InstitutionListFilter(SimpleListFilter):
    title = 'Організації'
    parameter_name = 'institution_id'
    
    def lookups(self, request, model_admin):
        institutions = Institution.objects.all()
        return [(inst.id, inst.name) for inst in institutions]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(institutions__id=self.value())
        return queryset

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone_number', 'email', 'institutions_list', 'sotial_role', 'ka_role')
    list_filter = (InstitutionListFilter,)
    search_fields = ['name', 'surname', 'email', 'institutions__name']
    
    def institutions_list(self, obj):
        return ", ".join([institution.name for institution in obj.institutions.all()])
    institutions_list.short_description = "Організації"


class EventParticipantInline(GenericTabularInline):
    model = EventParticipant
    extra = 1

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'conductor', 'event_date', 'location', 'created_at')
    list_filter = ('event_type', 'conductor',)
    search_fields = ['event_type__title', 'location', 'notes']
    inlines = [EventParticipantInline]
    
# class EventParticipantAdmin(admin.ModelAdmin):
#     list_display = ('event', 'participant')
#     search_fields = ('event__event_type__title',)
    
    

custom_admin_site.register(SotialRole, SotialRoleAdmin)
custom_admin_site.register(KaRole, KaRoleAdmin)
custom_admin_site.register(EventType, EventTypeAdmin)
custom_admin_site.register(Institution, InstitutionAdmin)
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Event, EventAdmin)