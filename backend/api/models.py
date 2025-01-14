from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    credit_hours = models.IntegerField()

    def __str__(self):
        return self.name

class Instructor(models.Model):
    name = models.CharField(max_length=255)
    available_days = ArrayField(models.CharField(max_length=10))

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class WorkingDay(models.Model):
    day = models.CharField(max_length=10)
    start_hr = models.CharField(max_length=5)
    end_hr = models.CharField(max_length=5)
    total_hours = models.CharField(max_length=5)

class Constraint(models.Model):
    working_days = models.ManyToManyField(WorkingDay)
    consecutive_subjects = models.JSONField()
    non_consecutive_subjects = models.JSONField()
