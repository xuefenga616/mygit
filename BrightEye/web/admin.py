#coding:utf-8
from django.contrib import admin

# Register your models here.
import models

class HostAdmin(admin.ModelAdmin):
    search_fields = ('hostname','ip_addr')
    list_display = ('hostname','ip_addr','port','system_type','enabled')

class HostUserAdmin(admin.ModelAdmin):
    list_display = ('auth_method','username')

class BindHostAdmin(admin.ModelAdmin):
    list_display = ('host','host_user','get_groups')
    list_filter = ('host','host_user','host_group')
    filter_horizontal = ('host_group',)
    #raw_id_fields = ('host','host_user')

class HostGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','name','department')
    filter_horizontal = ('host_groups','bind_hosts')

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id','user','host','action_type','cmd','date')
    list_filter = ('user','host','action_type','date')
    search_fields = ['user__user__username','host__host__hostname','host__host__ip_addr','cmd']

class TaskLogAdmin(admin.ModelAdmin):
    list_display = ('id','start_time','end_time','task_type','user','cmd','expire_time',)
    list_filter = ('task_type','user','start_time')

class TaskLogDetailAdmin(admin.ModelAdmin):
    list_display = ('child_of_task','bind_host','result','date')
    list_filter = ('child_of_task','result','date')

class TokenAdmin(admin.ModelAdmin):
    list_display = ('user','host','token','date','expire')
    readonly_fields = models.Token._meta.get_all_field_names()  #不可修改


admin.site.register(models.Hosts,HostAdmin)
admin.site.register(models.HostUsers,HostUserAdmin)
admin.site.register(models.BindHosts,BindHostAdmin)
admin.site.register(models.HostGroups,HostGroupAdmin)
admin.site.register(models.UserProfile,UserProfileAdmin)
admin.site.register(models.AuditLog,AuditLogAdmin)
admin.site.register(models.TaskLog,TaskLogAdmin)
admin.site.register(models.TaskLogDetail,TaskLogDetailAdmin)
admin.site.register(models.Token,TokenAdmin)
admin.site.register(models.IDC)
admin.site.register(models.Department)

