from django import forms
from data_tracker.courses.models import Course
from data_tracker.users.models import Mortals
import datetime
from dal import autocomplete

class RegistrationChartFilterForm(forms.Form):
    days = forms.IntegerField(label="Last N days", min_value=1, max_value=30, initial=7)
    
class CourseFilterForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=True,
        label="Course"
    )
MONTH_CHOICES = [(i, datetime.date(2025, i, 1).strftime("%B")) for i in range(1, 13)]

class PersonFilterForm(forms.Form):
    person = forms.ModelChoiceField(
        queryset=Mortals.objects.all(),
        required=True,
        # widget=autocomplete.ModelSelect2(url='mortals-autocomplete'),
        label="Person"
    )
    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        required=True,
        label="Month"
    )