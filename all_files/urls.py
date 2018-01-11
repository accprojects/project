from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='home'),
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^entertainment/$', views.entertainment, name='entertainment'),
    url(r'^home/$', views.post_list, name='home'),



    #url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
	#url(r'^post/new/$', views.post_new, name='post_new'),
]