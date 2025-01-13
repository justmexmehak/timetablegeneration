from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course, Constraint
from .serializers import CreateCourseSerializer, CourseSerializer, ConstraintSerializer, CreateConstraintSerializer

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

from django.http import JsonResponse

@api_view(['GET'])
def test_endpoint(request):
    return JsonResponse({'message': 'Test endpoint is working!'})