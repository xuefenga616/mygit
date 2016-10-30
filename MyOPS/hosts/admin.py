#coding:utf-8
from django.contrib import admin

# Register your models here.
import models
import auth_admin

class HostAdmin(admin.ModelAdmin):
    list_display = ('hostname','ip_addr','port','idc','system_type','enabled')
    search_fields = ('hostname','ip_addr')
    list_filter = ('idc','system_type')
    list_editable = ('enabled','port')  #可在admin页面修改
class HostUserAdmin(admin.ModelAdmin):
    list_display = ('auth_type','username')
class BindHostToUserAdmin(admin.ModelAdmin):
    list_display = ('host','host_user','get_groups')    #调用models里写的get_groups
    filter_horizontal = ('host_groups',)        #加此行后，选择更人性化

admin.site.register(models.UserProfile,auth_admin.UserProfileAdmin)
admin.site.register(models.Host,HostAdmin)
admin.site.register(models.HostGroup)
admin.site.register(models.HostUser,HostUserAdmin)
admin.site.register(models.BindHostToUser,BindHostToUserAdmin)
admin.site.register(models.IDC)
admin.site.register(models.TaskLog)
admin.site.register(models.TaskLogDetail)