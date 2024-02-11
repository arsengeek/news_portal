from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.views.generic import CreateView

class SingIn(CreateView):
    model = User
    form_class = RegistrationForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'