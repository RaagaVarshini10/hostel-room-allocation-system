from django.urls import path
from . import views

urlpatterns = [

    path("", views.hostel_list, name="hostel_list"),

    path(
        "hostel/<int:hostel_id>/",
        views.hostel_detail,
        name="hostel_detail"
    ),

    path(
        "room/<int:room_id>/",
        views.room_detail,
        name="room_detail"
    ),

    path(
        "book/<int:bed_id>/",
        views.book_bed,
        name="book_bed"
    ),

    path(
        "my-booking/",
        views.my_booking,
        name="my_booking"
    ),

    path(
        "apply/",
        views.apply_hostel,
        name="apply_hostel"
    ),

    path(
        "my-application/",
        views.my_application,
        name="my_application"
    ),

    # ADMIN
    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "admin-applications/",
        views.admin_applications,
        name="admin_applications"
    ),

    path(
        "approve/<int:application_id>/",
        views.approve_application,
        name="approve_application"
    ),

    path(
        "reject/<int:application_id>/",
        views.reject_application,
        name="reject_application"
    ),
    path(
    "admin-hostel/<int:hostel_id>/",
    views.admin_hostel_detail,
    name="admin_hostel_detail"
    ),
]