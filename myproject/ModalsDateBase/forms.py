from django import forms
from .models import Post, Catigory, Author
import datetime
from django.http import request


class CreatePost(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = [
            'title',
           'text_post',
           'content_post',
           'author'
        ]
    
class UpdatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            
           'text_post',
           'content_post'
        ]
        
class PostFormFilter(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = [
            'title',
            'content_post',
        ]
        
    def filter_posts(self):
        title = self.cleaned_data.get('title')
        content_post = self.cleaned_data.get('content_post')
        date = self.cleaned_data.get('date')

        posts = Post.objects.all()

        if title:
            posts = posts.filter(title__icontains=title)

        if content_post:
            posts = posts.filter(content_post__icontains=content_post)

        if date:
            posts = posts.filter(date__gte=date)

        return posts
