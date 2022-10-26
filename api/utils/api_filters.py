from api.models import Measurement
from assistme.settings import PAGE_SIZE
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination


class MeasurementFilter(filters.FilterSet):
    company = filters.NumberFilter(field_name='sensor__company',
                                   label='company')
    date = filters.DateTimeFromToRangeFilter(field_name='date')

    class Meta:
        model = Measurement
        fields = ['sensor', 'company', 'date']


class LargeResultsSetPagination(PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = page_size
    max_page_size = 5
