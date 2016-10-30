"""MyOPS URL Configuration

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
import views

urlpatterns = [
    url(r'^$', views.hosts_index,name="hosts"),
    url(r'^host_mgr/$', views.host_mgr,name="host_mgr"),
    url(r'^multi_cmd/$', views.multi_cmd,name="multi_cmd"),
    url(r'^submit_task/$', views.submit_task,name="submit_task"),
    url(r'^get_task_result/$', views.get_task_result,name="get_task_result"),

    url(r'^multi_file_transfer/$', views.multi_file_transfer,name="multi_file_transfer"),
    url(r'^file_upload/$', views.file_upload,name="file_upload"),
]
