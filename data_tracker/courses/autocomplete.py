from dal import autocomplete
from data_tracker.users.models import Mortals
from data_tracker.courses.models import Item, Video
from data_tracker.crm.models import User
from django.db.models import Q
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceAutoView

class ContentObjectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Video.objects.none()

        model_type = self.forwarded.get('model_type')

        if model_type == 'video':
            qs = Video.objects.all().order_by('title')
        elif model_type == 'article':
            qs = Item.objects.filter(type='article').order_by('title')
        elif model_type == 'exercise':
            qs = Item.objects.filter(type='exercise').order_by('title')
        else:
            qs = Video.objects.none()

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        return qs

class MortalsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Mortals.objects.none()

        qs = Mortals.objects.all()
        if self.q:
            qs = qs.filter(Q(first_name__icontains=self.q) | Q(last_name__icontains=self.q))

        return qs[:5]
    
class PeopleAutocomplete(Select2QuerySetSequenceAutoView):
    model_choice = [
        (Mortals,     'first_name'),
        (User,        'name'),
    ]
    mixup      = True       
    paginate_by = 50