from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    credit_hours = models.IntegerField()

    def __str__(self):
        return self.name

class Instructor(models.Model):
    name = models.CharField(max_length=255)
    available_days = models.JSONField()

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
        
class CourseAssignment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.section.name} - {self.course.name} - {self.instructor.name}"

class WorkingDay(models.Model):
    day = models.CharField(max_length=10)
    start_hr = models.CharField(max_length=5)
    end_hr = models.CharField(max_length=5)
    total_hours = models.CharField(max_length=5)

class Constraint(models.Model):
    working_days = models.ManyToManyField(WorkingDay)
    consecutive_subjects = models.JSONField()
    non_consecutive_subjects = models.JSONField()
