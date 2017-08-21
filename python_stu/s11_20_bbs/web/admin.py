from django.contrib import admin
import models

# Register your models here.
class CategroyAdmin(admin.ModelAdmin):
    list_display = ('id','name')
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title','author','publish_date','hidden')
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','parent_comment','comment','date')

admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.Category,CategroyAdmin)
admin.site.register(models.Comment,CommentAdmin)
admin.site.register(models.ThumbUp)
admin.site.register(models.UserProfile)
admin.site.register(models.UserGroup)

