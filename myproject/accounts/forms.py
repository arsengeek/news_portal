from django import forms
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='email')
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    
    class Meta():
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
        
class Signup(SignupForm):
    def save(self, request):
        user = super().save(request)
        commons = Group.objects.get(name='authors')
        user.groups.add(commons)
        return user