from django.contrib import admin

from posts.models import Post, Comment, PostView


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


