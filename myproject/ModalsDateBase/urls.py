from django.urls import path
from .views import News_list, News_Detail, SearchNews, create_post, search, EditPost, DeletPost, subscriptions

urlpatterns = [
    path('', News_list.as_view(), name='news_list'),
    path('search/', SearchNews.as_view(), name='search'),
    path('<int:pk>/', News_Detail.as_view(), name='news_detail'),
    path('create/',create_post, name='create_post'),
    path('<int:pk>/update', EditPost.as_view(), name='update_post'),
    path('<int:pk>/delete', DeletPost.as_view(),name='delete_post'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]