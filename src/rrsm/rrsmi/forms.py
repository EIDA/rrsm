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
            'pga_max',
            'pga_min',
            'pgv_max',
            'pgv_min',
        )
        labels = {
            'event_id': 'Event Id',
            'date_start': 'Start date (YYYY-MM-DD)',
            'date_end': 'End date (YYYY-MM-DD)',
            'magnitude_min': 'Magnitude minimum',
            'pga_max': 'Max. PGA PGA [cm/s^2]',
            'pga_min': 'Min. PGA PGA [cm/s^2]',
            'pgv_max': 'Max. PGV [cm/s]',
            'pgv_min': 'Min. PGV [cm/s]',
        }

