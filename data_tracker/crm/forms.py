from dal import autocomplete
from dal_select2_queryset_sequence.widgets import QuerySetSequenceSelect2
from django.urls import reverse

from data_tracker.users.models import Mortals
from data_tracker.crm.models import Institution, EventParticipant, User
from data_tracker.crm.autocomplete import LotsOfParticipantsAutocomplete


class EventParticipantForm(autocomplete.FutureModelForm):
    participant = autocomplete.Select2GenericForeignKeyModelField(
        model_choice=[
            (Mortals, 'first_name'),
            (User, 'name'),
            (Institution, 'name'),
        ],

        widget=QuerySetSequenceSelect2(
            'participant-autocomplete',
            attrs={
            'data-placeholder': 'Обери учасника',
            'data-allow-clear':  'true',
            'data-minimum-input-length': 0,
            }
        ),
        required=False,
    )

    class Meta:
        model   = EventParticipant
        verbose_name = "Учасник"
        verbose_name_plural = "Учасники"
        exclude = ('content_type', 'object_id')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        url = reverse('participant-autocomplete')
        w   = self.fields['participant'].widget

        setattr(w, 'url', url)
        w.attrs['data-autocomplete-light-url'] = url
        w.attrs['data-ajax--url']               = url