from django import forms
from .models import SearchEvent, SearchPeakMotions, SearchCombined


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
            'event_lat_min',
            'event_lat_max',
            'event_lon_min',
            'event_lon_max',
        )
        labels = {
            'event_id': 'Event Id',
            'date_start': 'Start date (YYYY-MM-DD)',
            'date_end': 'End date (YYYY-MM-DD)',
            'magnitude_min': 'Magnitude minimum',
            'network_code': 'Network code',
            'station_code': 'Station code',
            'event_lat_min': 'Event latitude minimum',
            'event_lat_max': 'Event latitude maximum',
            'event_lon_min': 'Event longitude minimum',
            'event_lon_max': 'Event longitude maximum',
        }
        help_texts = {
            'event_id': 'Alphanumeric string, e.g. "20180414_0000061"',
            'date_start': 'Date field, e.g. "2018-01-21"',
            'date_end': 'Date field, e.g. "2018-01-21"',
            'magnitude_min': 'Maximum 3 digits including 1 decimal place',
            'network_code': 'Alphanumeric string',
            'station_code': 'Alphanumeric string',
            'event_lat_min': 'Maximum 8 digits including 5 decimal places',
            'event_lat_max': 'Maximum 8 digits including 5 decimal places',
            'event_lon_min': 'Maximum 8 digits including 5 decimal places',
            'event_lon_max': 'Maximum 8 digits including 5 decimal places',
        }


class SearchPeakMotionsForm(forms.ModelForm):
    class Meta:
        model = SearchPeakMotions
        fields = (
            'pga_min',
            'pga_max',
            'pgv_min',
            'pgv_max',
        )
        labels = {
            'pga_min': 'PGA minimum [cm/s^2]',
            'pga_max': 'PGA maximum [cm/s^2]',
            'pgv_min': 'PGV minimum [cm/s]',
            'pgv_max': 'PGV maximum [cm/s]',
        }
        help_texts = {
            'pga_min': 'Maximum 10 digits including 5 decimal places',
            'pga_max': 'Maximum 10 digits including 5 decimal places',
            'pgv_min': 'Maximum 10 digits including 5 decimal places',
            'pgv_max': 'Maximum 10 digits including 5 decimal places',
        }


class SearchCombinedForm(forms.ModelForm):
    class Meta:
        model = SearchCombined
        fields = (
            'magnitude_min',
            'pga_min',
            'pga_max',
            'pgv_min',
            'pgv_max',
            'stat_lat_min',
            'stat_lat_max',
            'stat_lon_min',
            'stat_lon_max',
        )
        labels = {
            'magnitude_min': 'Magnitude minimum',
            'pga_min': 'PGA minimum [cm/s^2]',
            'pga_max': 'PGA maximum [cm/s^2]',
            'pgv_min': 'PGV minimum [cm/s]',
            'pgv_max': 'PGV maximum [cm/s]',
            'stat_lat_min': 'Station latitude minimum',
            'stat_lat_max': 'Station latitude maximum',
            'stat_lon_min': 'Station longitude minimum',
            'stat_lon_max': 'Station longitude maximum',
        }
        help_texts = {
            'magnitude_min': 'Maximum 3 digits including 1 decimal place',
            'pga_min': 'Maximum 10 digits including 5 decimal places',
            'pga_max': 'Maximum 10 digits including 5 decimal places',
            'pgv_min': 'Maximum 10 digits including 5 decimal places',
            'pgv_max': 'Maximum 10 digits including 5 decimal places',
            'stat_lat_min': 'Maximum 8 digits including 5 decimal places',
            'stat_lat_max': 'Maximum 8 digits including 5 decimal places',
            'stat_lon_min': 'Maximum 8 digits including 5 decimal places',
            'stat_lon_max': 'Maximum 8 digits including 5 decimal places',
        }
