from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course, Constraint
from .serializers import CreateCourseSerializer, CourseSerializer, ConstraintSerializer, CreateConstraintSerializer
from .utils import generate

@api_view(['POST'])
def post_course(request):
    if request.method == 'POST':
        serializer = CreateCourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_constraints(request):
    constraints = Constraint.objects.all()
    serializer = ConstraintSerializer(constraints, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def post_constraints(request):
    serializer = CreateConstraintSerializer(data=request.data)
    if serializer.is_valid():
        constraint = serializer.save()
        return Response(ConstraintSerializer(constraint).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def generate_timetable(request):
    constraints = Constraint.objects.all()
    courses = Course.objects.all()

    if not constraints.exists() or not courses.exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    constraints_data = ConstraintSerializer(constraints.last()).data
    courses_data = CourseSerializer(courses, many=True).data

    data = generate(constraints_data, courses_data)
    return JsonResponse(data, safe=False)

from django.http import JsonResponse

@api_view(['GET'])
def test_endpoint(request):
    return JsonResponse({'message': 'Test endpoint is working!'})