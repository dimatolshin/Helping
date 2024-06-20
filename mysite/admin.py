from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *


class UserUpgradeInline(admin.TabularInline):
    model = Profile
    extra = 1


admin.site.unregister(User)


@admin.register(Profile)
class UserUpgradeAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [UserUpgradeInline]


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(PodCategory)
class PodCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    pass


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    pass
