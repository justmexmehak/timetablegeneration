from django.urls import path
from .views import *

urlpatterns = [
    path('add-course/', post_course, name='post_course'),
    path('get-courses/', get_courses, name='get_courses'),
    path('get-constraints/', get_constraints, name='get_constraints'),
    path('add-constraints/', post_constraints, name='add_constraints'),
    path('test-endpoint/', test_endpoint, name='test_endpoint'),
]