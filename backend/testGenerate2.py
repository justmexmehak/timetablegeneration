import os
import django
import collections
from ortools.sat.python import cp_model

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
    # print(Instance)
    # print(InstanceSet)
    return InstanceSet, Rooms, PossibleRoomIds, VisitingFacultyAvailibility, timeSlotsPerDay, noOfDays

def create_model():
    InstanceSet, Rooms, PossibleRoomIds, VisitingFacultyAvailibility, timeSlotsPerDay, noOfDays = create_model_input()

    # Create Decision Variables
    model = cp_model.CpModel()

    Starts, RoomsDict, Days = {}, {}, {}

    maxRoomIndex = len(Rooms) - 1

    for i in InstanceSet:
        start_var = model.NewIntVar(0, 6, f'start of instance {InstanceSet.index(i)}')
        # end_var = model.NewIntVar(0, 8, f'end of instance {InstanceSet.index(i)}')
        room_var = model.NewIntVar(0, maxRoomIndex, f'room of instance {InstanceSet.index(i)}')
        day_var = model.NewIntVar(0, noOfDays - 1, f'day of instance {InstanceSet.index(i)}')
        Starts[i] = start_var
        # Ends[i] = end_var
        RoomsDict[i] = room_var
        Days[i] = day_var

    for a in InstanceSet:
        for b in InstanceSet:
            if a != b:
                # The same section can not have 2 classes at the same time
                if a.section == b.section or a.instructor == b.instructor:
                    same_day = model.NewBoolVar(f'same_day_{InstanceSet.index(a)}_{InstanceSet.index(b)}')
                    model.Add(Days[a] == Days[b]).OnlyEnforceIf(same_day)
                    model.Add(Days[a] != Days[b]).OnlyEnforceIf(same_day.Not())
                    # Prevent overlap only if the two classes are on the same day
                    # model.Add(Starts[a] >= Ends[b]).OnlyEnforceIf(same_day)
                    model.Add(Starts[b] >= Starts[a] + a.duration).OnlyEnforceIf(same_day)

    print(model.Validate())

    solver = cp_model.CpSolver()

    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
    # roomsClasses = {x: [] for x in Rooms}
        for i in InstanceSet:
            print(i.requirementId, i.course, i.duration, 'start = ', solver.Value(Starts[i]), 'day = ', solver.Value(Days[i]))

    timetable = {
        "7A": [],
        "7B": [],
        "7C": [],
        "7D": []
    }

    for i in InstanceSet:
        timetable[i.section.name].append({
            "id": i.requirementId,
            "name": i.course.name,
            "day": solver.Value(Days[i]),
            "startSlot": solver.Value(Starts[i]) + 1,
            "duration": i.duration,
            "room": Rooms[solver.Value(RoomsDict[i])].name
        })
    
    print(timetable)

create_model()




