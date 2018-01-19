from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.views.generic import View
from .forms import SignUpForm

def post_list(request):
    return render(request, 'all_files/home.html', {})

#def auth (request):
  #  return render(request, 'all_files/login.html', {})

def entertainment(request):
    return render(request, 'all_files/entertainment.html', {})     
 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'all_files/signup.html', {'form': form})

 