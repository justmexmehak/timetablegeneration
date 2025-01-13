from rest_framework import serializers
from .models import Course

class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'lectureno', 'duration', 'instructor_name', 'start_hr', 'end_hr']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'lectureno', 'duration', 'instructor_name', 'start_hr', 'end_hr']