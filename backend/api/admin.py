from django.contrib import admin
from .models import Course, WorkingDay, Constraint, Instructor, Room, Section, CourseAssignment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'credit_hours')

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'available_days',)
    
@admin.register(WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_hr', 'end_hr', 'total_hours')

@admin.register(Constraint)
class ConstraintAdmin(admin.ModelAdmin):
    list_display = ('id',)
    filter_horizontal = ('working_days',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(CourseAssignment)
class CourseAssignmentAdmin(admin.ModelAdmin):
    list_display = ('section', 'course', 'instructor')