from django.contrib import admin

from .models import Course, Group, Code, Attendance


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_filter = ('group__course__name', )
    list_display = ('user', 'created_at', 'course', 'group_name', )
