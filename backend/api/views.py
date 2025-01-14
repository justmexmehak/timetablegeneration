from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course, Constraint, Room, Instructor, CourseAssignment, Section
from .serializers import CreateCourseSerializer, CourseSerializer, ConstraintSerializer, InstructorSerializer, RoomSerializer, CourseAssignmentSerializer, SectionSerializer
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
def get_instructors(request):
    instructors = Instructor.objects.all()
    serializer = InstructorSerializer(instructors, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def post_instructor(request):
    serializer = InstructorSerializer(data=request.data)
    if serializer.is_valid():
        instructor = serializer.save()
        return Response(InstructorSerializer(instructor).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def post_room(request):
    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        room = serializer.save()
        return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_constraint(request):
    serializer = ConstraintSerializer(data=request.data)
    if serializer.is_valid():
        constraint = serializer.save()
        return Response(ConstraintSerializer(constraint).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_constraints(request):
    constraints = Constraint.objects.all()
    serializer = ConstraintSerializer(constraints, many=True)
    return Response(serializer.data)

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

@api_view(['POST'])
def assign_courses(request):
    section_name = request.data.get('section_name')
    assignments = request.data.get('assignments')

    if not section_name or not assignments:
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    section, created = Section.objects.get_or_create(name=section_name)

    for assignment in assignments:
        course_id = assignment.get('course')
        instructor_id = assignment.get('instructor')
        if not course_id or not instructor_id:
            continue
        CourseAssignment.objects.create(
            section=section,
            course_id=course_id,
            instructor_id=instructor_id
        )

    return Response({'message': 'Courses assigned successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def fake_generate_timetable(request):
    placeholder_data = {
        "Section A": [
            {
                "id": 1,
                "name": "Math",
                "startSlot": 1,
                "duration": 2,
                "roomNo": "101"
            },
            {
                "id": 2,
                "name": "Science",
                "startSlot": 3,
                "duration": 1,
                "roomNo": "102"
            }
        ],
        "Section B": [
            {
                "id": 1,
                "name": "History",
                "startSlot": 1,
                "duration": 2,
                "roomNo": "201"
            },
            {
                "id": 2,
                "name": "Geography",
                "startSlot": 3,
                "duration": 1,
                "roomNo": "202"
            }
        ]
    }
    return Response(placeholder_data)

from django.http import JsonResponse

@api_view(['GET'])
def test_endpoint(request):
    return JsonResponse({'message': 'Test endpoint is working!'})