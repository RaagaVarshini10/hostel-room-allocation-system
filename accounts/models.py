from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):

    YEAR_CHOICES = [
        (1, "1st Year"),
        (2, "2nd Year"),
        (3, "3rd Year"),
        (4, "4th Year"),
    ]

    DEPARTMENT_CHOICES = [
        ("IT", "Information Technology"),
        ("CSE", "Computer Science Engineering"),
        ("ECE", "Electronics and Communication Engineering"),
        ("EEE", "Electrical and Electronics Engineering"),
        ("MECH", "Mechanical Engineering"),
        ("CIVIL", "Civil Engineering"),
        ("OTHER", "Other"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    phone = models.CharField(max_length=15)
    register_number = models.CharField(max_length=30, unique=True)
    department = models.CharField(
        max_length=20,
        choices=DEPARTMENT_CHOICES
    )
    year = models.IntegerField(
        choices=YEAR_CHOICES
    )

    def __str__(self):
        return f"{self.user.username} - {self.register_number}"