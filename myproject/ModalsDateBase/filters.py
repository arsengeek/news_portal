from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post, Catigory

class PostFilter(FilterSet):
    categories = ModelChoiceFilter(
        field_name = 'content_post',
        queryset = Catigory.objects.all(),
        label = 'Categories'
    )
    time_post = DateTimeFilter(
        field_name='time_post',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
    
    class Meta:
        model = Post
        fields = {
            'title' : ['exact'],
        }