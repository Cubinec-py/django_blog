from django.contrib import admin
from django.contrib.admin import TabularInline, StackedInline

from .models import Post, PostCustomUser, Comment


class PostInline(StackedInline):
    model = Post
    extra = 0
    ordering = ['-posted']


class CommentInline(TabularInline):
    model = Comment
    extra = 0


@admin.register(PostCustomUser)
class PostUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_superuser')
    inlines = [PostInline]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'creat_date', 'date_updated', 'posted')
    list_filter = ['author', 'category']
    actions = ['post']
    inlines = [CommentInline]
    ordering = ['-posted']

    def post(self, request, queryset):
        if Post.objects.filter(posted=False):
            queryset.update(posted=True)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'published']
    list_filter = ['post', 'name']
    actions = ['publish']
    ordering = ['-published']

    def publish(self, request, queryset):
        if Comment.objects.filter(published=False):
            queryset.update(published=True)
