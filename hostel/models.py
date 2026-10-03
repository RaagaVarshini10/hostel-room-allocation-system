from django.db import models
from django.contrib.auth.models import User


class Hostel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    features = models.TextField()
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE,
        related_name="rooms"
    )
    room_number = models.CharField(max_length=10)
    sharing_type = models.IntegerField()

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"

    @property
    def total_beds(self):
        return self.beds.count()

    @property
    def available_beds(self):
        return self.beds.filter(is_booked=False).count()


class Bed(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="beds"
    )
    bed_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room.room_number} - Bed {self.bed_number}"


class HostelApplication(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hostel_applications"
    )

    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    room_preference = models.IntegerField(
        choices=[
            (3, "3 Sharing"),
            (4, "4 Sharing"),
        ]
    )

    reason = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.hostel.name}"


class Booking(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    bed = models.OneToOneField(
        Bed,
        on_delete=models.CASCADE
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.bed}"