"""s11_20_bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from web import urls as web_urls
from web_chat import urls as chat_urls
from web import views as web_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^web/', include(web_urls)),
    url(r'^chat/', include(chat_urls)),
    url(r'^login/$',web_views.acc_login,name='login'),
    url(r'^logout/$',web_views.acc_logout,name='logout')
]
