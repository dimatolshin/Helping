from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *


class UserUpgradeInline(admin.TabularInline):
    model = UserUpgrade
    extra = 1


admin.site.unregister(User)


@admin.register(UserUpgrade)
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
