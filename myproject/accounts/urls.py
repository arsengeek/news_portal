from django.urls import path
from .views import SingIn

urlpatterns = [
    path('signup/', SingIn.as_view(),name='sign')
]