import django_filters
from .models import Vehicle


class VehicleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    seats_min = django_filters.NumberFilter(field_name='seats', lookup_expr='gte')
    seats_max = django_filters.NumberFilter(field_name='seats', lookup_expr='lte')
    price_min = django_filters.NumberFilter(field_name='price_per_day', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price_per_day', lookup_expr='lte')
    year = django_filters.NumberFilter(field_name='year', lookup_expr='exact')
    has_driver = django_filters.BooleanFilter(field_name='has_driver')
    available_today = django_filters.BooleanFilter(field_name='available_today')
    has_ac = django_filters.BooleanFilter(field_name='has_ac')

    class Meta:
        model = Vehicle
        fields = [
            'category', 'seats_min', 'seats_max',
            'price_min', 'price_max', 'year',
            'has_driver', 'available_today', 'has_ac', 'is_active',
        ]
