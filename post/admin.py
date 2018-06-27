from django.contrib import admin

from post.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')


admin.site.register(Post, PostAdmin)
