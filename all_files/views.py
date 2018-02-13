from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import authenticate  
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
#from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.shortcuts import resolve_url
from django.conf import settings
from django.http import HttpResponseRedirect, QueryDict
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.shortcuts import get_current_site
from django.views import generic
from django.views.generic import View
from .forms import SignUpForm 
from django.core.signals import request_finished
from django.dispatch import receiver
from django.utils.module_loading import import_string
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
import datetime
import json
import os 
import hashlib
import inspect


def home(request):
    #if request.user.is_authenticated():
        #write_block(request.user.username, 'open home')
    return render(request, 'all_files/home.html', {}) 
  
def entertainment(request):
    #if request.user.is_authenticated():
        #write_block(request.user.username, 'open entertainment')
    return render(request, 'all_files/entertainment.html', {})     
 
def get_hash(filename):
    blockchain_dir = './blocks/'
    file = open(blockchain_dir + filename,'rb').read()
    return hashlib.md5(file).hexdigest()

def write_block(username, act, ip, prev_hash=''):

    blockchain_dir = './blocks/'

    files = os.listdir(blockchain_dir)
    files = sorted([int(i) for i in files])

    last_file = files[-1]

    filename = str(last_file + 1)

    prev_hash = get_hash(str(last_file))

    data = {'name': username,
            'ip': ip,
            'act':  act,
            'time': str(datetime.datetime.now()),
            'prev_hash': prev_hash}

    with open(blockchain_dir + filename, 'w') as file:
        json.dump(data, file, indent=4,ensure_ascii=False)
        
###############################################################        
#--------------------------------------------------------------
###############################################################        
  
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'all_files/signup.html', {'form': form})

 
def check(request, params, ip):
    UserModel = get_user_model() 

    username = str(params['username'])
    password = str(params['password'])
    #if User.objects.filter(username=username).exists():
    #username = kwargs.get(UserModel.USERNAME_FIELD) #хочу получить логин (в каком виде доходит)
    try:
        user = UserModel._default_manager.get_by_natural_key(username) #при прямой передаче логина возвращается пустой объект
    except:
        user = None


    #try:
    if user is not None and user.check_password(password):
        return user  
    elif user is not None:
        write_block(params, 'Incorrect password', ip ) 
        return None
    elif user is None: 
        return redirect('signup')

    #except UserModel.DoesNotExist: 
        
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
        #UserModel().set_password(password)

 
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))
    

    if request.method == "POST":
        form = authentication_form(request, data=request.POST) 
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
            
            # Okay, security check complete. Log the user in.  
            auth_login(request, form.get_user())
            #write_block(form.cleaned_data.get('username'), 'login') 
            
            return HttpResponseRedirect(redirect_to)
        else:
            check(request, request.POST, request.environ['REMOTE_ADDR'])
    else:
        form = authentication_form(request)


    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)
 

def logout(request, next_page=None,
           template_name='all_files/home.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)

    if next_page is not None:
        next_page = resolve_url(next_page)

    if (redirect_field_name in request.POST or
            redirect_field_name in request.GET):
        next_page = request.POST.get(redirect_field_name,
                                     request.GET.get(redirect_field_name))
        # Security check -- don't allow redirection to a different host.
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = request.path

    if next_page:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page)

    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Logged out')
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)

###############################################################        
#--------------------------------------------------------------
###############################################################        






###############################################################        
#--------------------------------------------------------------
###############################################################        
