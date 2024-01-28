from django.urls import path
from .views import News_list, News_Detail

urlpatterns = [
    path('', News_list.as_view(), name='news_list'),
    path('<int:pk>/', News_Detail.as_view(), name='news_detail')
]