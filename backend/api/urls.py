from django.urls import path
from .views import *

urlpatterns = [
    path('add-course/', post_course, name='post_course'),
    path('get-courses/', get_courses, name='get_courses'),
    path('get-instructors/', get_instructors, name='get_instructors'),
    path('add-instructor/', post_instructor, name='post_instructor'),
    path('generate-timetable/', generate_timetable, name='generate_timetable'),
    path('test-endpoint/', test_endpoint, name='test_endpoint'),
    path('get-rooms/', get_rooms, name='get_rooms'),
    path('add-room/', post_room, name='post_room'),
    path('assign-courses/', assign_courses, name='assign_courses'),
     path('add-constraint/', add_constraint, name='add_constraint'),
    path('get-constraints/', get_constraints, name='get_constraints'),
]