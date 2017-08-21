
from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'index/$', views.index),
    url(r'cache/$', views.cache_page),
    url(r'home/$', views.home),
    url(r'login/$', views.login),
    url(r'logout/$', views.logout),
]
