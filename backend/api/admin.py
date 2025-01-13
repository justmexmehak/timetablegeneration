from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'lectureno', 'duration', 'instructor_name', 'start_hr', 'end_hr')