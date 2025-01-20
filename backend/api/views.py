from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course, Constraint, Room, Instructor, CourseAssignment, Section
from .serializers import CreateCourseSerializer, CourseSerializer, ConstraintSerializer, InstructorSerializer, RoomSerializer, CourseAssignmentSerializer, SectionSerializer
from .utils import generate
import collections
from ortools.sat.python import cp_model

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
    data = create_model()
    return JsonResponse(data)

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
                "name": "MIS",
                "day": "Wednesday",
                "startSlot": 1,
                "duration": 3,
                "roomNo": "FF-104"
            },
            {
                "id": 2,
                "name": "PST",
                "day": "Wednesday",
                "startSlot": 8,
                "duration": 2,
                "roomNo": "FF-147"
            },
            {
                "id": 3,
                "name": "PDC",
                "day": "Thursday",
                "startSlot": 7,
                "duration": 3,
                "roomNo": "CSLab1"
            },
            {
                "id": 4,
                "name": "DevOps",
                "day": "Saturday",
                "startSlot": 1,
                "duration": 3,
                "roomNo": "CSLab1"
            },
            {
                "id": 5,
                "name": "DL",
                "day": "Saturday",
                "startSlot": 4,
                "duration": 3,
                "roomNo": "FF-104"
            }
        ],
        "Section B": [
            {
                "id": 1,
                "name": "History",
                "day": "Monday",
                "startSlot": 1,
                "duration": 2,
                "roomNo": "201"
            },
            {
                "id": 2,
                "name": "Geography",
                "day": "Tuesday",
                "startSlot": 3,
                "duration": 1,
                "roomNo": "202"
            }
        ]
    }
    return Response(placeholder_data)

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
        # Define possible start times that encourage spacing
        Starts[i] = model.NewIntVar(0, timeSlotsPerDay - i.duration, f'start_{i.requirementId}')
        RoomsDict[i] = model.NewIntVar(0, len(Rooms) - 1, f'room_{i.requirementId}')
        Days[i] = model.NewIntVar(0, noOfDays - 1, f'day_{i.requirementId}')

     # 2. Basic Scheduling Constraints
    for a in InstanceSet:
        for b in InstanceSet:
            if a.requirementId < b.requirementId:
                # Only add constraints for same section or instructor
                if a.section == b.section or a.instructor == b.instructor:
                    # Must be on different days or not overlap if on same day
                    same_day = model.NewBoolVar(f'same_day_{a.requirementId}_{b.requirementId}')
                    model.Add(Days[a] == Days[b]).OnlyEnforceIf(same_day)
                    model.Add(Days[a] != Days[b]).OnlyEnforceIf(same_day.Not())
                    
                    # If on same day, ensure no overlap with spacing
                    model.Add(Starts[a] + a.duration + 1 <= Starts[b]).OnlyEnforceIf(same_day)

    # 3. Fixed Room Assignment using AddAllowedAssignments
    for i in InstanceSet:
        if i.course in AssignedRooms:
            allowed_rooms = [idx for idx, room in enumerate(Rooms) 
                           if room in AssignedRooms[i.course]]
            if allowed_rooms:
                model.AddAllowedAssignments([RoomsDict[i]], [[room] for room in allowed_rooms])

    # 4. Time Distribution Hints
    # Encourage spacing between classes
    for section in Sections:
        section_classes = [i for i in InstanceSet if i.section == section]
        for day in range(noOfDays):
            day_classes = []
            for i in section_classes:
                is_on_day = model.NewBoolVar(f'section_{section}_day_{day}_class_{i.requirementId}')
                model.Add(Days[i] == day).OnlyEnforceIf(is_on_day)
                model.Add(Days[i] != day).OnlyEnforceIf(is_on_day.Not())
                day_classes.append((is_on_day, i))
            
            # Limit classes per day
            model.Add(sum(is_on_day for is_on_day, _ in day_classes) <= 3)

            # Try to encourage spacing between classes on the same day
            for idx, (is_on_day1, class1) in enumerate(day_classes):
                for class2 in section_classes[idx + 1:]:
                    is_on_day2 = model.NewBoolVar(f'section_{section}_day_{day}_class_{class2.requirementId}')
                    model.Add(Days[class2] == day).OnlyEnforceIf(is_on_day2)
                    model.Add(Days[class2] != day).OnlyEnforceIf(is_on_day2.Not())
                    
                    # If both classes are on this day, ensure spacing
                    both_on_day = model.NewBoolVar(f'both_on_day_{class1.requirementId}_{class2.requirementId}')
                    model.Add(is_on_day1 + is_on_day2 == 2).OnlyEnforceIf(both_on_day)
                    model.Add(is_on_day1 + is_on_day2 < 2).OnlyEnforceIf(both_on_day.Not())
                    
                    # Try to maintain at least 2 slots between classes
                    model.Add(Starts[class2] >= Starts[class1] + class1.duration + 2).OnlyEnforceIf(both_on_day)

    print(f"Model validation: {model.Validate()}")

    
    solver = cp_model.CpSolver()

    status = solver.Solve(model)

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0
    print("Starting solver...")
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Found a solution!")
        print_solution(solver, InstanceSet, Starts, Days, RoomsDict, Rooms)
    else:
        print(f"No solution found. Status code: {status}")
        print("\nSolver statistics:")
        print(solver.ResponseStats())
        return {"error": "no solution found"}

    timetable = {
        "7A": [],
        "7B": [],
        "7C": [],
        "7D": []
    }

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    for i in InstanceSet:
        timetable[i.section.name].append({
            "id": i.requirementId,
            "name": i.course.name,
            "day": days[solver.Value(Days[i])],
            "startSlot": solver.Value(Starts[i]) + 1,
            "duration": i.duration,
            "room": Rooms[solver.Value(RoomsDict[i])].name,
            "instructor": i.instructor.name
        })
    
    print(timetable)
    return timetable

def print_solution(solver, InstanceSet, Starts, Days, RoomsDict, Rooms):
    schedule = collections.defaultdict(lambda: collections.defaultdict(list))
    
    for i in InstanceSet:
        day = solver.Value(Days[i])
        start = solver.Value(Starts[i])
        room = Rooms[solver.Value(RoomsDict[i])]
        
        schedule[day][room].append({
            'course': i.course,
            'section': i.section,
            'instructor': i.instructor,
            'start': start,
            'end': start + i.duration - 1
        })
    
    for day in sorted(schedule.keys()):
        print(f"\nDay {day + 1}")
        print("=" * 50)
        for room in sorted(schedule[day].keys()):
            print(f"\nRoom: {room}")
            for class_ in sorted(schedule[day][room], key=lambda x: x['start']):
                print(f"  {class_['start']}-{class_['end']}: {class_['course']} "
                      f"(Section {class_['section']}, {class_['instructor']})")



from django.http import JsonResponse

@api_view(['GET'])
def test_endpoint(request):
    return JsonResponse({'message': 'Test endpoint is working!'})