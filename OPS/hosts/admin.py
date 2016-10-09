#coding:utf-8
from django.contrib import admin

# Register your models here.
import models
import auth_admin

class HostAdmin(admin.ModelAdmin):  # 自定义admin
    list_display = ('hostname', 'ip_addr', 'port', 'idc', 'system_type', 'enabled')#显示
    search_fields = ('hostname', 'ip_addr') #搜索
    list_filter = ('idc', 'system_type')    #多级过滤
    list_editable = ('enabled', 'ip_addr')  #在线编辑
class HostUserAdmin(admin.ModelAdmin):  # 自定义admin
    list_display = ('auth_type', 'username', 'password')#显示
class BindHostToUserAdmin(admin.ModelAdmin):  # 自定义admin
    list_display = ('host', 'host_user', 'get_groups')#显示
    filter_horizontal = ('host_groups',)    #轻松显示

admin.site.register(models.UserProfile, auth_admin.UserProfileAdmin)
admin.site.register(models.Host, HostAdmin)
admin.site.register(models.HostGroup)
admin.site.register(models.HostUser, HostUserAdmin)
admin.site.register(models.BindHostToUser, BindHostToUserAdmin)
admin.site.register(models.IDC)
admin.site.register(models.TaskLog)
admin.site.register(models.TaskLogDetail)
