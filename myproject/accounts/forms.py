from django import forms
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail,mail_admins
        
class Signup(SignupForm):
    def save(self, request):
        user = super().save(request)
        commons = Group.objects.get(name='authors')
        user.groups.add(commons)
        
        send_mail (
            subject='Thanks for singup',
            message=f'Succes singup to user {user.username}',
            recipient_list=[user.email],
            from_email=None,
        )
        
        mail_admins(
            subject='New User',
            message=f'User {user.username} singup'
        )
        return user
    
    