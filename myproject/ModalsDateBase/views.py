from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView,DetailView, UpdateView, DeleteView
from .models import Post, Author, Subscription
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from .filters import *
from .forms import CreatePost, PostFormFilter, UpdatePost
from django import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin , PermissionRequiredMixin
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef


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
    
class SearchNews(ListView):
    model = Post
    ordering = ''
    template_name = 'search.html' 
    context_object_name = 'search'
    
    def get_queryset(self):
        queryset =  super().get_queryset()
        self.filterset = PostFilter(self.request.POST, queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context
    
    def post(self, request, *args, **kwargs):
        # Handle POST request logic here
        # For example, perform form submission or other operations
        return self.get(request, *args, **kwargs)
        
    
class News_Detail(DetailView):
    model = Post
    ordering = 'text_post'
    template_name = 'detail.htm'
    context_object_name =  'one_post'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class EditPost(PermissionRequiredMixin,UpdateView):
    permission_required = ('ModalsDateBase.change_post')
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

# def check_perm(user):
#     if user.has_perm('create_post'):
#         return True
#     else:
#         return False


def is_author(user):
    return user.groups.filter(name='authors').exists()


def create_post(request):
    if request.method == 'POST':
        form = CreatePost(request.POST)
        if form.is_valid():
            current_user = request.user
            author = Author.objects.get(user=current_user)
            post = form.save(commit=False)
            post.author = author
            post.save()
            return HttpResponseRedirect('/news/')
    else:
        form = CreatePost()
    return render(request, 'create_post.html', {'form': form})

def search(request):
    form = PostFormFilter()
    if request.method == 'POST':
        return HttpResponseRedirect('/news/')
        
        
    return render(request, 'search.html', {'form': form})


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Catigory.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Catigory.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category')
    return renderв(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )