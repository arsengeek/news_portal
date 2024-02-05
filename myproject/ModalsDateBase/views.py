from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView,DetailView, UpdateView, DeleteView
from .models import Post
from datetime import datetime
from django.http import HttpResponse, request, HttpResponseRedirect
from .filters import *
from .forms import CreatePost, PostFormFilter, UpdatePost
from django import forms
from django.urls import reverse_lazy

class News_list(ListView):
    model = Post
    ordering = ''
    template_name = 'project.htm'
    context_object_name = 'post'
    paginate_by=10
    
    
    def check_title_exist(self, value):
        instance = PostFilter({'title': value}, queryset=Post.objects.all())
        
        exist = instance.qs.exists()
        
        return exist
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = PostFilter(self.request.GET, queryset)
        return self.form.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context
    
class SearchNews(forms.ModelForm):
    form_class = PostFormFilter
    model = Post
    template_name = 'search.html' 
    
class News_Detail(DetailView):
    model = Post
    ordering = 'text_post'
    template_name = 'detail.htm'
    context_object_name =  'one_post'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class EditPost(UpdateView):
    form_class = UpdatePost
    model = Post
    template_name = 'update_post.html'
    
class DeletPost(DeleteView):
    model = Post 
    success_url = reverse_lazy('news_list')
    template_name = 'delete_post.html'

def multiply(request):
    number = request.GET.get('number')
    multiplier = request.GET.get('multiplier')
    
    try:
       result = int(number) * int(multiplier)
       html = f"<html><body>{number}*{multiplier}={result}</body></html>"
    except (ValueError, TypeError):
        html = f"<html><body>Invalid input.</body></html>"

    return HttpResponse(html)

def create_post(request):
    if request.method == 'POST':
        form = CreatePost(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')
    form = CreatePost()
    return render(request, 'create_post.html', {'form': form})

def search(request):
    form = PostFormFilter()
    if request.method == 'POST':
        return HttpResponseRedirect('/news/')
        
        
    return render(request, 'search.html', {'form': form})