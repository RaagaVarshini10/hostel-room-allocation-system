from django.contrib import admin
from .models import Hostel, Room, Bed, Booking

admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(Bed)
admin.site.register(Booking)
