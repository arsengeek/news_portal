from typing import Any
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Post
from datetime import datetime

class News_list(ListView):
    model = Post
    ordering = ''
    template_name = 'project.htm'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context
    
class News_Detail(DetailView):
    model = Post
    ordering = 'text_post'
    template_name = 'detail.htm'
    context_object_name =  'one_post'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context
