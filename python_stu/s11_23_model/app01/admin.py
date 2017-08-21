from django.contrib import admin

# Register your models here.
import models

admin.site.register(models.MyUser)
admin.site.register(models.News)
admin.site.register(models.Favor)
admin.site.register(models.HostAdmin2)
admin.site.register(models.Host)
