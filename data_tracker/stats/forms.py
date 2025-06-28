from django import forms
from data_tracker.courses.models import Course

class RegistrationChartFilterForm(forms.Form):
    days = forms.IntegerField(label="Last N days", min_value=1, max_value=30, initial=7)
    
class CourseFilterForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=True,
        label="Course"
    )