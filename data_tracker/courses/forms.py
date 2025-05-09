from dal import autocomplete
from django import forms
from django.contrib.contenttypes.models import ContentType
from data_tracker.courses.models import Item, Video, BugReport
from data_tracker.users.models import Mortals
from data_tracker.crm.models import User
from dal_select2_queryset_sequence.widgets import QuerySetSequenceSelect2

class BugReportAdminForm(forms.ModelForm):
    model_type = forms.ChoiceField(
        choices=[
        ('video', 'Video'),
        ('article', 'Article'),
        ('exercise', 'Exercise')
        ],
        label="Content type"
    )

    content_object = forms.ModelChoiceField(
        queryset=Video.objects.none(),
        widget=autocomplete.ModelSelect2(
            url='content-object-autocomplete',
            forward=['model_type'],
            attrs={
                'data-placeholder': 'Select content object...',
                'data-minimum-input-length': 0,
            }
        ),
        label="Content title",
        required=True,
    )
    
    assigned_to = forms.ModelChoiceField(
        queryset=Mortals.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='mortals-autocomplete',
            attrs={
                'data-placeholder': 'Search users...',
                'data-minimum-input-length': 0,
            }
        ),
        required=False,
        label="Assign to"
    )
    
    reported_by = autocomplete.Select2GenericForeignKeyModelField(
        model_choice=[
            (Mortals, 'first_name'),
            (User, 'name'),
        ],
        widget=QuerySetSequenceSelect2(
            url='people-autocomplete',
            attrs={
                'data-placeholder': 'Search people...',
                'data-minimum-input-length': 0,
            }
        ),
        required=False,
        label="Reported by"
    )

    class Meta:
        model = BugReport
        fields = ['model_type', 'content_object', 'bug_type', 'title', 'description', 'assigned_to', 'reported_by']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        model_type = self.data.get('model_type') or self.initial.get('model_type')
        if not model_type and self.instance and self.instance.pk:
            model_type = self.instance.content_type.model

        if model_type == 'video':
            self.fields['model_type'].initial = model_type
        elif model_type == 'item': 
            if self.instance.content_object.type == 'article':
                self.fields['model_type'].initial = 'article'
            elif self.instance.content_object.type == 'exercise':
                self.fields['model_type'].initial = 'exercise'
                
        print(self.fields['model_type'].initial)
        
        if model_type == 'video':
            self.fields['content_object'].queryset = Video.objects.all()
        elif model_type == 'article':
            self.fields['content_object'].queryset = Item.objects.filter(type='article')
        elif model_type == 'exercise':
            self.fields['content_object'].queryset = Item.objects.filter(type='exercise')
        else:
            self.fields['content_object'].queryset = Video.objects.none()

        # Set initial object if editing
        if self.instance and self.instance.pk:
            self.fields['content_object'].initial = self.instance.content_object
            print(self.fields['content_object'].initial)
            
    def save(self, commit=True):
        instance = super().save(commit=False)

        content_object = self.cleaned_data.get('content_object')
        if content_object:
            instance.content_type = ContentType.objects.get_for_model(content_object.__class__)
            instance.object_id = content_object.pk
            
        reported_by = self.cleaned_data.get('reported_by')
        if reported_by:
            instance.reported_by_content_type = ContentType.objects.get_for_model(reported_by.__class__)
            instance.reported_by_object_id = reported_by.pk

        if commit:
            instance.save()
            self.save_m2m()

        return instance

    
    def clean(self):
        cleaned_data = super().clean()
        model_type = cleaned_data.get('model_type')
        object_id = self.data.get('content_object')

        if not model_type or not object_id:
            raise forms.ValidationError("Please select both type and object.")

        if model_type == 'video':
            model = Video
            queryset = model.objects.all()
        elif model_type == 'article':
            model = Item
            queryset = model.objects.filter(type='article')
        elif model_type == 'exercise':
            model = Item
            queryset = model.objects.filter(type='exercise')
        else:
            raise forms.ValidationError("Invalid model type.")

        try:
            obj = queryset.get(pk=object_id)
        except model.DoesNotExist:
            raise forms.ValidationError("Selected object does not exist.")

        cleaned_data['content_type'] = ContentType.objects.get_for_model(model)
        cleaned_data['object_id'] = obj.pk
        cleaned_data['content_object'] = obj
        return cleaned_data