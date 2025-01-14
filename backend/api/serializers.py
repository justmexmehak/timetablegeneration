from rest_framework import serializers
from .models import Course, WorkingDay, Constraint, Instructor, Room

class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'credit_hours']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'credit_hours']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name']

class CreateInstructorSerializer(serializers.ModelSerializer):
    available_days = serializers.SlugRelatedField(
        many=True,
        slug_field='day',
        queryset=WorkingDay.objects.all()
    )

    class Meta:
        model = Instructor
        fields = ['name', 'available_days']

class InstructorSerializer(serializers.ModelSerializer):
    available_days = WorkingDaySerializer(many=True)

    class Meta:
        model = Instructor
        fields = ['id', 'name', 'available_days']

class WorkingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingDay
        fields = '__all__'

class ConstraintSerializer(serializers.ModelSerializer):
    working_days = WorkingDaySerializer(many=True)

    class Meta:
        model = Constraint
        fields = '__all__'

class CreateConstraintSerializer(serializers.ModelSerializer):
    working_days = WorkingDaySerializer(many=True)

    class Meta:
        model = Constraint
        fields = '__all__'

    def create(self, validated_data):
        working_days_data = validated_data.pop('working_days')
        constraint = Constraint.objects.create(**validated_data)
        for working_day_data in working_days_data:
            working_day, created = WorkingDay.objects.get_or_create(**working_day_data)
            constraint.working_days.add(working_day)
        return constraint