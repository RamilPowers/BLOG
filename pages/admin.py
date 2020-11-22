from django.contrib import admin
from .models import Post, Comment, About


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created', 'updated', 'status')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    ordering = ['status', 'created', 'updated']
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'text', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    list_editable = ['active']
admin.site.register(Comment, CommentAdmin)

class AboutAdmin(admin.ModelAdmin):
    list_display = ['updated']
admin.site.register(About, AboutAdmin)