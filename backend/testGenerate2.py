import os
import django
import collections

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django
django.setup()

from api.models import Constraint, Course, Instructor, Room, CourseAssignment, Section

def create_model_input():
    courses = Course.objects.all()
    instructors = Instructor.objects.all()
    course_assignments = CourseAssignment.objects.all()
    rooms = Room.objects.all()
    sections = Section.objects.all()
    constraints = Constraint.objects.all()

    # print("Courses:", courses)
    # print("Instructors:", instructors)
    # print("Course Assignments:", course_assignments)
    # print("Rooms:", rooms)
    # print("Sections:", sections)
    # print("Constraints:", constraints)

    timeSlotsPerDay = 9
    noOfDays = 6

    RequirementSet = []
    # (section, course, instructor, duration)
    for course_assignment in course_assignments:
        course = course_assignment.course
        instructor = course_assignment.instructor
        section = course_assignment.section
        duration = course.credit_hours
        RequirementSet.append((section, course, instructor, duration))

    # print("RequirementSet:", RequirementSet)

    Rooms = [room for room in rooms]

    # print("Rooms:", Rooms)  

    AssignedRooms = {}
    # {"course": [rooms]}
    for constraint in constraints:
        course = constraint.course
        rooms = constraint.rooms.all()
        AssignedRooms[course] = rooms
    
    # print("AssignedRooms:", AssignedRooms)

    VisitingFacultyAvailibility = {}
    # {"instructor": [days]}
    for instructor in instructors:
        VisitingFacultyAvailibility[instructor] = instructor.available_days

    # print("VisitingFacultyAvailibility:", VisitingFacultyAvailibility)

    PossibleRooms = {
        (course, room): (room in AssignedRooms[course]) if course in AssignedRooms
        else all((room, k) not in AssignedRooms.items() for k in courses if k != course) for course in courses for room in Rooms
    }
    # print(PossibleRooms)
    PossibleRoomIds = {course: {Rooms.index(room) for room in Rooms if PossibleRooms[course, room]} for course in courses}
    # print(PossibleRoomIds)

    # Create instances
    Instance = collections.namedtuple('instance_data', 'section course instructor duration requirementId')
    InstanceSet = [Instance(section=r[0], course=r[1], instructor=r[2], duration=r[3], requirementId=z) for z, r in enumerate(RequirementSet)]
    print(Instance)
    print(InstanceSet)

create_model_input()
