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

        if self.data:
            model_type = self.data.get('model_type')
        elif self.instance and self.instance.pk:
            model_type = self.instance.content_type.model
            if model_type == 'item':
                if self.instance.content_object.type == 'article':
                    model_type = 'article'
                elif self.instance.content_object.type == 'exercise':
                    model_type = 'exercise'
        else:
            model_type = self.initial.get('model_type')

        if model_type == 'video':
            self.fields['content_object'].queryset = Video.objects.all()
        elif model_type == 'article':
            self.fields['content_object'].queryset = Item.objects.filter(type='article')
        elif model_type == 'exercise':
            self.fields['content_object'].queryset = Item.objects.filter(type='exercise')
        else:
            self.fields['content_object'].queryset = Video.objects.none()
        
        if self.instance and self.instance.pk:
            self.fields['content_object'].initial = self.instance.content_object
            self.fields['model_type'].initial = model_type
            self.fields['reported_by'].initial = self.instance.reported_by
            print(f"On init: {model_type}")
            print(f"On init: {self.fields['content_object'].initial}")
            
    def save(self, commit=True):
        instance = super().save(commit=False)
        content_object = self.cleaned_data.get('content_object')
        print(f"On save: {self.cleaned_data.get('model_type')}")
        print(f"On save: {content_object}")
        
        if content_object:
            instance.content_type = ContentType.objects.get_for_model(content_object.__class__)
            instance.object_id = content_object.pk

        if commit:
            instance.save()
            self.save_m2m()

        return instance

    
    def clean(self):
        cleaned_data = super().clean()
        model_type = cleaned_data.get('model_type')
        content_object = cleaned_data.get('content_object')
        print(f"On clean: {model_type}")
        print(f"On clean: {content_object}")     
           
        if not model_type or not content_object:
            raise forms.ValidationError("Please select both type and object.")
        
        if model_type == 'video' and not isinstance(content_object, Video):
            raise forms.ValidationError("Selected object is not a Video.")
        elif model_type == 'article' and not (isinstance(content_object, Item) and content_object.type == 'article'):
            raise forms.ValidationError("Selected object is not an Article.")
        elif model_type == 'exercise' and not (isinstance(content_object, Item) and content_object.type == 'exercise'):
            raise forms.ValidationError(f"Selected object is not an Exercise.")

        cleaned_data['content_type'] = ContentType.objects.get_for_model(content_object.__class__)
        cleaned_data['object_id'] = content_object.pk
        cleaned_data['content_object'] = content_object
        return cleaned_data
    
class BugReportInlineForm(forms.ModelForm):
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.fields['reported_by'].initial = self.instance.reported_by
            
    class Meta:
        model = BugReport
        fields = ['bug_type', 'title', 'description', 'assigned_to', 'reported_by']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.content_type = ContentType.objects.get_for_model(self._parent_obj.__class__)
        instance.object_id = self._parent_obj.pk

        if commit:
            instance.save()
        return instance
