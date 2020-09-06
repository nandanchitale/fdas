from django.db import models

from django.contrib.auth.models import User

class Faculty(models.Model):
    username = models.CharField(max_length=40)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return str(self.username)


def student_directory_path(instance, filename):
    name, ext = filename.split(".")
    # + "_" + instance.branch + "_" + instance.year + "_" + instance.section
    name = instance.registration_id
    filename = name + '.' + ext
    return 'Student_Images/{}/{}/{}/{}'.format(instance.branch, instance.year, instance.section, filename)


class Student(models.Model):

    BRANCH = (
        ('CSE', 'CSE'),
        ('IT', 'IT'),
        ('ECE', 'ECE'),
        ('CHEM', 'CHEM'),
        ('MECH', 'MECH'),
        ('EEE', 'EEE'),
    )
    YEAR = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    SECTION = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )

    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    registration_id = models.CharField(max_length=200, null=True)
    branch = models.CharField(max_length=100, null=True, choices=BRANCH)
    year = models.CharField(max_length=100, null=True, choices=YEAR)
    section = models.CharField(max_length=100, null=True, choices=SECTION)
    profile_pic = models.ImageField(
        upload_to=student_directory_path, null=True, blank=True)

    def __str__(self):
        return str(self.registration_id)


class Attendence(models.Model):
    # faculty = models.ForeignKey(Faculty, null = True, on_delete= models.SET_NULL)
    # student = models.ForeignKey(Student, null = True, on_delete= models.SET_NULL)
    Faculty_Name = models.CharField(max_length=200, null=True, blank=True)
    Student_ID = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)
    branch = models.CharField(max_length=200, null=True)
    year = models.CharField(max_length=200, null=True)
    section = models.CharField(max_length=200, null=True)
    period = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True, default='Absent')

    def __str__(self):
        return str(self.Student_ID + "_" + str(self.date) + "_" + str(self.period))
