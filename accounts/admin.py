from django.contrib import admin

from .models import *

admin.site.register(AcademicEntity)


class InLineAcademicEntity(admin.StackedInline):
    """Inline academic entity form for the user admin form"""
    model = AcademicEntity
    extra = 1
    max_num = 1


class InLineUserDetail(admin.StackedInline):
    """Inline user detail form for the user admin form"""
    model = UserDetail
    extra = 1
    max_num = 1
    inlines = [InLineAcademicEntity]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User admin form"""
    inlines = [InLineUserDetail]
