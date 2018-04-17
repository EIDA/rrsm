from django import forms
from .models import SearchEvent


class SearchEventsForm(forms.ModelForm):
    class Meta:
        model = SearchEvent
        fields = (
            'event_id',
            'date_start',
            'date_end',
            'magnitude_min',
            'network_code',
            'station_code',
            'level',
        )
        labels = {
            'event_id': 'Event Id',
            'date_start': 'Start date (YYYY-MM-DD)',
            'date_end': 'End date (YYYY-MM-DD)',
            'magnitude_min': 'Magnitude minimum'
        }
