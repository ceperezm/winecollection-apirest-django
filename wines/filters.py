import django_filters
from .models import Wine

class WineFilter(django_filters.FilterSet):
    total_sulfur_dioxide_min = django_filters.NumberFilter(field_name='attribute__total_sulfur_dioxide', lookup_expr='gte')
    total_sulfur_dioxide_max = django_filters.NumberFilter(field_name='attribute__total_sulfur_dioxide', lookup_expr='lte')
    
    fixed_acidity_min = django_filters.NumberFilter(field_name='attribute__fixed_acidity', lookup_expr='gte')
    fixed_acidity_max = django_filters.NumberFilter(field_name='attribute__fixed_acidity', lookup_expr='lte')
    
    volatile_acidity_min = django_filters.NumberFilter(field_name='attribute__volatile_acidity', lookup_expr='gte')
    volatile_acidity_max = django_filters.NumberFilter(field_name='attribute__volatile_acidity', lookup_expr='lte')
    
    free_sulfur_dioxide_min = django_filters.NumberFilter(field_name='attribute__free_sulfur_dioxide', lookup_expr='gte')
    free_sulfur_dioxide_max = django_filters.NumberFilter(field_name='attribute__free_sulfur_dioxide', lookup_expr='lte')
    
    citric_acid_min = django_filters.NumberFilter(field_name='attribute__citric_acid', lookup_expr='gte')
    citric_acid_max = django_filters.NumberFilter(field_name='attribute__citric_acid', lookup_expr='lte')
    
    residual_sugar_min = django_filters.NumberFilter(field_name='attribute__residual_sugar', lookup_expr='gte')
    residual_sugar_max = django_filters.NumberFilter(field_name='attribute__residual_sugar', lookup_expr='lte')
    
    chlorides_min = django_filters.NumberFilter(field_name='attribute__chlorides', lookup_expr='gte')
    chlorides_max = django_filters.NumberFilter(field_name='attribute__chlorides', lookup_expr='lte')
    
    density_min = django_filters.NumberFilter(field_name='attribute__density', lookup_expr='gte')
    density_max = django_filters.NumberFilter(field_name='attribute__density', lookup_expr='lte')
    
    pH_min = django_filters.NumberFilter(field_name='attribute__pH', lookup_expr='gte')
    pH_max = django_filters.NumberFilter(field_name='attribute__pH', lookup_expr='lte')
    
    sulphates_min = django_filters.NumberFilter(field_name='attribute__sulphates', lookup_expr='gte')
    sulphates_max = django_filters.NumberFilter(field_name='attribute__sulphates', lookup_expr='lte')
    
    alcohol_min = django_filters.NumberFilter(field_name='attribute__alcohol', lookup_expr='gte')
    alcohol_max = django_filters.NumberFilter(field_name='attribute__alcohol', lookup_expr='lte')
    
    variety = django_filters.CharFilter(field_name='variety', lookup_expr='iexact')
    harvest_year_min = django_filters.NumberFilter(field_name='harvest_year', lookup_expr='gte')
    harvest_year_max = django_filters.NumberFilter(field_name='harvest_year', lookup_expr='lte')
    harvest_year = django_filters.NumberFilter(field_name='harvest_year', lookup_expr='exact')

    class Meta:
        model = Wine
        fields = ['provider']
