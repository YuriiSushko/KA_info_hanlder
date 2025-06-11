from dal_select2_queryset_sequence.views import Select2QuerySetSequenceAutoView
from data_tracker.users.models import Mortals
from data_tracker.crm.models import User, Institution


class LotsOfParticipantsAutocomplete(Select2QuerySetSequenceAutoView):
    model_choice = [
        (Mortals,     'first_name'),
        (User,        'name'),
        (Institution, 'name'),
    ]
    mixup      = True       
    paginate_by = 50
    