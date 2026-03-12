from django.db import models
from django.contrib.auth.models import User


class Hostel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    features = models.TextField()

    def __str__(self):
        return self.name


class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    sharing_type = models.IntegerField()  # 3 or 4

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"


class Bed(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room.room_number} - Bed {self.bed_number}"


class Booking(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    bed = models.OneToOneField(Bed, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.bed}"
