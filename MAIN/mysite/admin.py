from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *


class ChildrenInline(admin.TabularInline):
    model = Children
    extra = 1



class ParentInline(admin.StackedInline):
    model = Parent
    can_delete = False


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [ParentInline, ChildrenInline]


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    inlines = [ChildrenInline]


@admin.register(Children)
class ChildrenAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
