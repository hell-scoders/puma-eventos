from django.contrib import admin
from .models import *

admin.site.register(AcademicEntity)


class InLineAcademicEntity(admin.StackedInline):
    model = AcademicEntity
    extra = 1
    max_num = 1


class InLineUserDetail(admin.StackedInline):
    model = UserDetail
    extra = 1
    max_num = 1
    inlines = [InLineAcademicEntity]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [InLineUserDetail]
