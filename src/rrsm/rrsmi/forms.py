from django import forms
from .models import \
    SearchEvent, SearchPeakMotions, SearchCombined, SearchCustom, \
    COORD_INTEGERS, COORD_DECIMALS, \
    PGA_PGV_INTEGERS, PGA_PGV_DECIMALS, \
    MAG_INTEGERS, MAG_DECIMALS

LABEL_EVENT_ID = 'Event Id'
LABEL_DATE_START = 'Start date (YYYY-MM-DD)'
LABEL_DATE_END = 'End date (YYYY-MM-DD)'
LABEL_MAGNITUDE_MIN = 'Magnitude minimum'
LABEL_NETWORK_CODE = 'Network code'
LABEL_STATION_CODE = 'Station code'
LABEL_PGA_MIN = 'PGA minimum [cm/s^2]'
LABEL_PGA_MAX = 'PGA maximum [cm/s^2]'
LABEL_PGV_MIN = 'PGV minimum [cm/s]'
LABEL_PGV_MAX = 'PGV maximum [cm/s]'
LABEL_STAT_LAT_MIN = 'Station latitude minimum'
LABEL_STAT_LAT_MAX = 'Station latitude maximum'
LABEL_STAT_LON_MIN = 'Station longitude minimum'
LABEL_STAT_LON_MAX = 'Station longitude maximum'
LABEL_EVENT_LAT_MIN = 'Event latitude minimum'
LABEL_EVENT_LAT_MAX = 'Event latitude maximum'
LABEL_EVENT_LON_MIN = 'Event longitude minimum'
LABEL_EVENT_LON_MAX = 'Event longitude maximum'

TEXT_EVENT_ID = 'Alphanumeric string, e.g. "20180414_0000061"'
TEXT_DATE_START = 'Date field, e.g. "2018-01-21"'
TEXT_DATE_END = 'Date field, e.g. "2018-01-21"'
TEXT_MAGNITUDE_MIN = 'Maximum {} digits including {} decimal place'.format(
    MAG_INTEGERS + MAG_DECIMALS, MAG_DECIMALS
)
TEXT_NETWORK_CODE = 'Alphanumeric string'
TEXT_STATION_CODE = 'Alphanumeric string'
TEXT_PGA_MIN = 'Maximum {} digits including {} decimal places'.format(
    PGA_PGV_INTEGERS + PGA_PGV_DECIMALS, PGA_PGV_DECIMALS
)
TEXT_PGA_MAX = 'Maximum {} digits including {} decimal places'.format(
    PGA_PGV_INTEGERS + PGA_PGV_DECIMALS, PGA_PGV_DECIMALS
)
TEXT_PGV_MIN = 'Maximum {} digits including {} decimal places'.format(
    PGA_PGV_INTEGERS + PGA_PGV_DECIMALS, PGA_PGV_DECIMALS
)
TEXT_PGV_MAX = 'Maximum {} digits including {} decimal places'.format(
    PGA_PGV_INTEGERS + PGA_PGV_DECIMALS, PGA_PGV_DECIMALS
)
TEXT_STAT_LAT_MIN = 'Maximum {} digits including {} decimal places'.format(
    COORD_INTEGERS + COORD_DECIMALS, COORD_DECIMALS
)
TEXT_STAT_LAT_MAX = 'Maximum {} digits including {} decimal places'.format(
    COORD_INTEGERS + COORD_DECIMALS, COORD_DECIMALS
)
TEXT_STAT_LON_MIN = 'Maximum {} digits including {} decimal places'.format(
    COORD_INTEGERS + COORD_DECIMALS, COORD_DECIMALS
)
TEXT_STAT_LON_MAX = 'Maximum {} digits including {} decimal places'.format(
    COORD_INTEGERS + COORD_DECIMALS, COORD_DECIMALS
)
TEXT_EVENT_LAT_MIN = 'Maximum {} digits including {} decimal places'.format(
    COORD_INTEGERS + COORD_DECIMALS, COORD_DECIMALS
)
TEXT_EVENT_LAT_MAX = 'Maximum {} digits including {} decimal places'.format(
    COORD_INTEGERS + COORD_DECIMALS, COORD_DECIMALS
)
TEXT_EVENT_LON_MIN = 'Maximum {} digits including {} decimal places'.format(
    COORD_INTEGERS + COORD_DECIMALS, COORD_DECIMALS
)
TEXT_EVENT_LON_MAX = 'Maximum {} digits including {} decimal places'.format(
    COORD_INTEGERS + COORD_DECIMALS, COORD_DECIMALS
)


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
            'event_id': LABEL_EVENT_ID,
            'date_start': LABEL_DATE_START,
            'date_end': LABEL_DATE_END,
            'magnitude_min': LABEL_MAGNITUDE_MIN,
            'network_code': LABEL_NETWORK_CODE,
            'station_code': LABEL_STATION_CODE,
            'event_lat_min': LABEL_EVENT_LAT_MIN,
            'event_lat_max': LABEL_EVENT_LAT_MAX,
            'event_lon_min': LABEL_EVENT_LON_MIN,
            'event_lon_max': LABEL_EVENT_LON_MAX,
        }
        help_texts = {
            'event_id': TEXT_EVENT_ID,
            'date_start': TEXT_DATE_START,
            'date_end': TEXT_DATE_END,
            'magnitude_min': TEXT_MAGNITUDE_MIN,
            'network_code': TEXT_NETWORK_CODE,
            'station_code': TEXT_STATION_CODE,
            'event_lat_min': TEXT_EVENT_LAT_MIN,
            'event_lat_max': TEXT_EVENT_LAT_MAX,
            'event_lon_min': TEXT_EVENT_LON_MIN,
            'event_lon_max': TEXT_EVENT_LON_MAX,
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
            'pga_min': LABEL_PGA_MIN,
            'pga_max': LABEL_PGA_MAX,
            'pgv_min': LABEL_PGV_MIN,
            'pgv_max': LABEL_PGV_MAX,
        }
        help_texts = {
            'pga_min': TEXT_PGA_MIN,
            'pga_max': TEXT_PGA_MAX,
            'pgv_min': TEXT_PGV_MIN,
            'pgv_max': TEXT_PGV_MAX,
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
            'event_lat_min',
            'event_lat_max',
            'event_lon_min',
            'event_lon_max',
        )
        labels = {
            'magnitude_min': LABEL_MAGNITUDE_MIN,
            'pga_min': LABEL_PGA_MIN,
            'pga_max': LABEL_PGA_MAX,
            'pgv_min': LABEL_PGV_MIN,
            'pgv_max': LABEL_PGV_MAX,
            'stat_lat_min': LABEL_STAT_LAT_MIN,
            'stat_lat_max': LABEL_STAT_LAT_MAX,
            'stat_lon_min': LABEL_STAT_LON_MIN,
            'stat_lon_max': LABEL_STAT_LON_MAX,
            'event_lat_min': LABEL_EVENT_LAT_MIN,
            'event_lat_max': LABEL_EVENT_LAT_MAX,
            'event_lon_min': LABEL_EVENT_LON_MIN,
            'event_lon_max': LABEL_EVENT_LON_MAX,
        }
        help_texts = {
            'magnitude_min': TEXT_MAGNITUDE_MIN,
            'pga_min': TEXT_PGA_MIN,
            'pga_max': TEXT_PGA_MAX,
            'pgv_min': TEXT_PGV_MIN,
            'pgv_max': TEXT_PGV_MAX,
            'stat_lat_min': TEXT_STAT_LAT_MIN,
            'stat_lat_max': TEXT_STAT_LAT_MAX,
            'stat_lon_min': TEXT_STAT_LON_MIN,
            'stat_lon_max': TEXT_STAT_LON_MAX,
            'event_lat_min': TEXT_EVENT_LAT_MIN,
            'event_lat_max': TEXT_EVENT_LAT_MAX,
            'event_lon_min': TEXT_EVENT_LON_MIN,
            'event_lon_max': TEXT_EVENT_LON_MAX,
        }


class SearchCustomForm(forms.ModelForm):
    class Meta:
        model = SearchCustom
        fields = (
            'event_id',
            'date_start',
            'date_end',
            'magnitude_min',
            'network_code',
            'station_code',
            'pga_min',
            'pga_max',
            'pgv_min',
            'pgv_max',
            'stat_lat_min',
            'stat_lat_max',
            'stat_lon_min',
            'stat_lon_max',
            'event_lat_min',
            'event_lat_max',
            'event_lon_min',
            'event_lon_max',        
        )
        labels = {
            'event_id': LABEL_EVENT_ID,
            'date_start': LABEL_DATE_START,
            'date_end': LABEL_DATE_END,
            'magnitude_min': LABEL_MAGNITUDE_MIN,
            'network_code': LABEL_NETWORK_CODE,
            'station_code': LABEL_STATION_CODE,
            'pga_min': LABEL_PGA_MIN,
            'pga_max': LABEL_PGA_MAX,
            'pgv_min': LABEL_PGV_MIN,
            'pgv_max': LABEL_PGV_MAX,
            'stat_lat_min': LABEL_STAT_LAT_MIN,
            'stat_lat_max': LABEL_STAT_LAT_MAX,
            'stat_lon_min': LABEL_STAT_LON_MIN,
            'stat_lon_max': LABEL_STAT_LON_MAX,
            'event_lat_min': LABEL_EVENT_LAT_MIN,
            'event_lat_max': LABEL_EVENT_LAT_MAX,
            'event_lon_min': LABEL_EVENT_LON_MIN,
            'event_lon_max': LABEL_EVENT_LON_MAX,
        }
        help_texts = {
            'event_id': TEXT_EVENT_ID,
            'date_start': TEXT_DATE_START,
            'date_end': TEXT_DATE_END,
            'magnitude_min': TEXT_MAGNITUDE_MIN,
            'network_code': TEXT_NETWORK_CODE,
            'station_code': TEXT_STATION_CODE,
            'pga_min': TEXT_PGA_MIN,
            'pga_max': TEXT_PGA_MAX,
            'pgv_min': TEXT_PGV_MIN,
            'pgv_max': TEXT_PGV_MAX,
            'stat_lat_min': TEXT_STAT_LAT_MIN,
            'stat_lat_max': TEXT_STAT_LAT_MAX,
            'stat_lon_min': TEXT_STAT_LON_MIN,
            'stat_lon_max': TEXT_STAT_LON_MAX,
            'event_lat_min': TEXT_EVENT_LAT_MIN,
            'event_lat_max': TEXT_EVENT_LAT_MAX,
            'event_lon_min': TEXT_EVENT_LON_MIN,
            'event_lon_max': TEXT_EVENT_LON_MAX,
        }
