from django.contrib import admin

from .models import (
    Hostel,
    Room,
    Bed,
    Booking,
    HostelApplication
)


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "location",
    )

    search_fields = (
        "name",
        "location",
    )
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "room_number",
        "hostel",
        "sharing_type",
        "total_beds_display",
        "available_beds_display",
    )

    list_filter = (
        "hostel",
        "sharing_type",
    )

    search_fields = (
        "room_number",
        "hostel__name",
    )

    @admin.display(description="Total Beds")
    def total_beds_display(self, obj):
        return obj.total_beds

    @admin.display(description="Available Beds")
    def available_beds_display(self, obj):
        return obj.available_beds
@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):

    list_display = (
        "bed_number",
        "room",
        "status_display",
        "student_display",
    )

    list_filter = (
        "is_booked",
        "room__hostel",
    )

    search_fields = (
        "bed_number",
        "room__room_number",
        "room__hostel__name",
        "booking__student__username",
    )

    @admin.display(description="Status")
    def status_display(self, obj):

        if obj.is_booked:
            return "Occupied"

        return "Available"

    @admin.display(description="Student")
    def student_display(self, obj):

        booking = getattr(obj, "booking", None)

        if booking:
            return booking.student.username

        return "—"
@admin.register(HostelApplication)
class HostelApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "hostel",
        "room_preference",
        "status",
        "applied_at",
    )

    list_filter = (
        "status",
        "hostel",
    )

    search_fields = (
        "student__username",
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "bed",
        "booked_at",
    )