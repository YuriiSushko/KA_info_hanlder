from data_tracker.admin_site import custom_admin_site
from django.contrib import admin
from data_tracker.crm.models import User, Institution, SotialRole, KaRole, Event, EventType, EventParticipant, ContactInfoInline
from data_tracker.crm.forms import EventParticipantForm
from django.contrib.admin import SimpleListFilter
from django.contrib.contenttypes.admin import GenericTabularInline

class SotialRoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ['title']

class KaRoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ['title']

class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ['title']

class ContactInfoInlineAdmin(GenericTabularInline):
    model = ContactInfoInline
    extra = 1
    
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'role', 'add_info')
    search_fields = ['name', 'email']
    inlines = [ContactInfoInlineAdmin]
    
    def add_info(self, obj):
        qs    = obj.contact_info.all()
        total = qs.count()

        infos = [str(ci.contact_info) for ci in qs[:3]]
        result = ", ".join(infos)
        if total > 3:
            result += ", …"
        return result
    add_info.short_description = "Додаткова інформація"
    
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
    list_display = ('name', 'surname', 'phone_number', 'email', 'institutions_list', 'sotial_role', 'ka_role', 'add_info')
    list_filter = (InstitutionListFilter,)
    search_fields = ['name', 'surname', 'email', 'institutions__name']
    inlines = [ContactInfoInlineAdmin]
    
    def institutions_list(self, obj):
        return ", ".join([institution.name for institution in obj.institutions.all()])
    institutions_list.short_description = "Організації"
    
    def add_info(self, obj):
        qs    = obj.contact_info.all()
        total = qs.count()

        infos = [str(ci.contact_info) for ci in qs[:3]]
        result = ", ".join(infos)
        if total > 3:
            result += ", …"
        return result
    add_info.short_description = "Додаткова інформація"


class EventParticipantInline(admin.TabularInline):
    model = EventParticipant
    form = EventParticipantForm
    extra = 1
    fields = ('participant',) 
    exclude = ('content_type','object_id')

class EventAdmin(admin.ModelAdmin):
    autocomplete_fields = ['conductor']
    list_display = ('event_type', 'conductor', 'event_date', 'location', 'created_at', 'recent_participants')
    list_filter = ('event_type', 'conductor',)
    search_fields = ['event_type__title', 'location', 'notes']
    inlines = [EventParticipantInline]
    
    def recent_participants(self, obj):
        qs    = obj.participant.all()
        total = qs.count()

        names = [str(ep.participant) for ep in qs[:3]]
        result = ", ".join(names)
        if total > 3:
            result += ", …"
        return result
    recent_participants.short_description = "Учасники"

    
# class EventParticipantAdmin(admin.ModelAdmin):
#     list_display = ('event', 'participant')
#     search_fields = ('event__event_type__title',)
    
    

custom_admin_site.register(SotialRole, SotialRoleAdmin)
custom_admin_site.register(KaRole, KaRoleAdmin)
custom_admin_site.register(EventType, EventTypeAdmin)
custom_admin_site.register(Institution, InstitutionAdmin)
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Event, EventAdmin)