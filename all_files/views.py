from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm


def post_list(request):
    return render(request, 'all_files/home.html', {})

def auth (request):
    return render(request, 'all_files/auth.html', {})

def entertainment(request):
    return render(request, 'all_files/entertainment.html', {})    

