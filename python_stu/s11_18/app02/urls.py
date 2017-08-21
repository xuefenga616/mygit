
from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'user_list/$', views.user_list),
    url(r'user_list2/$', views.user_list2),
    url(r'ajax_data/$', views.ajax_data),

]
