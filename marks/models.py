from django.db import models
from django.contrib.auth.models import User

CLASS_CHOICES = (
    ('High School', 'High School'),
    ('Intermediate', 'Intermediate'),
)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="")  # Default value is an empty string
    roll_number = models.CharField(max_length=20, default="")  # Default value is an empty string
    dob = models.DateField(default="2000-01-01")  # Default value is January 1, 2000
    class_in = models.CharField(max_length=20, choices=CLASS_CHOICES, default="High School")
    
    def __str__(self):
        return self.name


CLASS_CHOICES = (
    ('High School', 'High School'),
    ('Intermediate', 'Intermediate'),
)

class Subject(models.Model):
    name = models.CharField(max_length=100)
    class_in = models.CharField(max_length=20, choices=CLASS_CHOICES, default='High School')

    def __str__(self):
        return self.name

    @classmethod
    def create_high_school_subjects(cls):
        high_school_subjects = ['Math', 'Science', 'Social Studies', 'English', 'Hindi']
        for subject_name in high_school_subjects:
            cls.objects.create(name=subject_name, class_in='High School')

    @classmethod
    def create_intermediate_subjects(cls):
        intermediate_subjects = ['Physics', 'Chemistry', 'Math', 'English', 'Hindi']
        for subject_name in intermediate_subjects:
            cls.objects.create(name=subject_name, class_in='Intermediate')

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ['student', 'subject']

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name}: {self.marks_obtained}"
