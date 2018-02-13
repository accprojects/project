from django.conf.urls import url, include
from . import views
#from django.contrib.auth.views import login
#from django.contrib.auth import authenticate, login

urlpatterns = [
    #url(r'^login/$', views.UserFormView.as_view(), name='login'),
    #url(r'^login/$', views.UserFormView.as_view(), name='signup'),
    url(r'^$', views.home, name='home'), 
    url(r'^entertainment/$', views.entertainment, name='entertainment'),
    url(r'^home/$', views.home, name='home'), 
   # url(r'^accounts/login/$', views.login, name='all_files/login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
#    url(r'^accounts/logout/$', views.logout, {'next_page': 'all_files/login.html'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    #url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
	#url(r'^post/new/$', views.post_new, name='post_new'),
]