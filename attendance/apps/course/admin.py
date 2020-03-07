from django.contrib import admin

from .models import Course, Group, Code


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass
