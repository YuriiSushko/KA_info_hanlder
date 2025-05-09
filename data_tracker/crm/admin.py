from data_tracker.admin_site import custom_admin_site
from django.contrib import admin
from data_tracker.crm.models import User, Institution, SotialRole, KaRole, Event, EventType, EventParticipant, ContactInfoInline, PhoneNumber, OrgClass
from data_tracker.users.models import Mortals
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
    
class PhoneNumberInline(GenericTabularInline):
    model = PhoneNumber
    extra = 1
    
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number_filter', 'email', 'person_list', 'role', 'get_class_orgs', 'add_info')
    list_filter = ('role', 'org_class') 
    search_fields = ['name', 'email']
    inlines = [ContactInfoInlineAdmin, PhoneNumberInline]
    
    def person_list(self, obj):
        return ", ".join([str(person) for person in obj.people.all()])
    person_list.short_description = "Персони"
    
    def add_info(self, obj):
        qs = obj.contact_info.exclude(value__isnull=True).exclude(value__exact='')
        total = qs.count()

        infos = [ci.value for ci in qs[:3]]
        result = ", ".join(infos)
        if total > 3:
            result += ", …"
        return result or "—"
    add_info.short_description = "Додатковий контакт"
    
    def phone_number_filter(self, obj):
        numbers = []
        if obj.phone_number:
            numbers.append(obj.phone_number)
        
        extras_qs = obj.phone_numbers.all()
        numbers.extend(pn.phone_number for pn in extras_qs if pn.phone_number)

        total = len(numbers)
        shown = numbers[:2]
        text  = ", ".join(shown)
        if total > 2:
            text += ", …"
        return text
    phone_number_filter.short_description = "Номер телефону"
    
    def get_class_orgs(self, obj):
        return ", ".join([org_class.name for org_class in obj.org_class.all()])
    get_class_orgs.short_description = 'Клас організації'
    
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
    list_display = ('name', 'surname','phone_number_filter','email', 'institutions_list', 'sotial_role', 'ka_role', 'add_info')
    list_filter = (InstitutionListFilter,)
    list_display_links = ['name', 'surname']
    search_fields = ['name', 'surname', 'email', 'institutions__name']
    inlines = [ContactInfoInlineAdmin, PhoneNumberInline]
    
    def institutions_list(self, obj):
        return ", ".join([institution.name for institution in obj.institutions.all()])
    institutions_list.short_description = "Організації"
    
    def add_info(self, obj):
        qs = obj.contact_info.exclude(value__isnull=True).exclude(value__exact='')
        total = qs.count()

        infos = [ci.value for ci in qs[:3]]
        result = ", ".join(infos)
        if total > 3:
            result += ", …"
        return result or "—"
    add_info.short_description = "Додатковий контакт"
    
    def phone_number_filter(self, obj):
        numbers = []
        if obj.phone_number:
            numbers.append(obj.phone_number)
        
        extras_qs = obj.phone_numbers.all()
        numbers.extend(pn.phone_number for pn in extras_qs if pn.phone_number)

        total = len(numbers)
        shown = numbers[:2]
        text  = ", ".join(shown)
        if total > 2:
            text += ", …"
        return text
    phone_number_filter.short_description = "Номер телефону"


class EventParticipantInline(admin.TabularInline):
    model = EventParticipant
    form = EventParticipantForm
    extra = 1
    fields = ('participant',) 
    exclude = ('content_type','object_id')
    
class ConductorListFilter(SimpleListFilter):
    title = 'хто проводить'
    parameter_name = 'conductor_id'
    
    def lookups(self, request, model_admin):
        conductors = Event.objects.exclude(conductor__isnull=True).values_list('conductor', flat=True).distinct()
        return [(user.pk, str(user)) for user in Mortals.objects.filter(pk__in=conductors)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(conductor__id=self.value())
        return queryset

class EventAdmin(admin.ModelAdmin):
    autocomplete_fields = ['conductor']
    list_display = ('event_type', 'conductor', 'event_date', 'location', 'created_at', 'recent_participants')
    list_display_links = ['conductor']
    list_filter = ('event_type', ConductorListFilter,)
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
    

custom_admin_site.register(SotialRole, SotialRoleAdmin)
custom_admin_site.register(KaRole, KaRoleAdmin)
custom_admin_site.register(EventType, EventTypeAdmin)
custom_admin_site.register(Institution, InstitutionAdmin)
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Event, EventAdmin)
custom_admin_site.register(OrgClass)