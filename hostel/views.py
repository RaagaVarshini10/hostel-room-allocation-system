from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import (
    Hostel,
    Room,
    Bed,
    Booking,
    HostelApplication
)


def hostel_list(request):
    hostels = Hostel.objects.all()

    return render(
        request,
        "hostel_list.html",
        {"hostels": hostels}
    )


def hostel_detail(request, hostel_id):

    hostel = get_object_or_404(
        Hostel,
        id=hostel_id
    )

    rooms = Room.objects.filter(
        hostel=hostel
    )

    return render(
        request,
        "hostel_detail.html",
        {
            "hostel": hostel,
            "rooms": rooms
        }
    )


def room_detail(request, room_id):

    room = get_object_or_404(
        Room,
        id=room_id
    )

    beds = Bed.objects.filter(
        room=room
    )

    return render(
        request,
        "room_detail.html",
        {
            "room": room,
            "beds": beds
        }
    )


@login_required
def book_bed(request, bed_id):

    bed = get_object_or_404(
        Bed,
        id=bed_id
    )

    if bed.is_booked:
        messages.error(
            request,
            "This bed is already booked."
        )
        return redirect(
            "room_detail",
            room_id=bed.room.id
        )

    if Booking.objects.filter(
        student=request.user
    ).exists():

        messages.warning(
            request,
            "You already have an allocation."
        )

        return redirect("my_booking")

    bed.is_booked = True
    bed.save()

    Booking.objects.create(
        student=request.user,
        bed=bed
    )

    messages.success(
        request,
        "Bed successfully allocated!"
    )

    return redirect("my_booking")


@login_required
def my_booking(request):

    booking = Booking.objects.filter(
        student=request.user
    ).first()

    return render(
        request,
        "my_booking.html",
        {
            "booking": booking
        }
    )

@login_required
def apply_hostel(request):

    if HostelApplication.objects.filter(
        student=request.user,
        status="Pending"
    ).exists():

        messages.warning(
            request,
            "You already have a pending application."
        )

        return redirect("my_application")

    if HostelApplication.objects.filter(
        student=request.user,
        status="Approved"
    ).exists():

        messages.info(
            request,
            "You already have an approved application."
        )

        return redirect("my_booking")

    hostels = Hostel.objects.all()

    # Add availability information for each hostel
    for hostel in hostels:

        hostel.available_3_sharing = Bed.objects.filter(
            room__hostel=hostel,
            room__sharing_type=3,
            is_booked=False
        ).count()

        hostel.available_4_sharing = Bed.objects.filter(
            room__hostel=hostel,
            room__sharing_type=4,
            is_booked=False
        ).count()

    if request.method == "POST":

        hostel_id = request.POST.get("hostel")
        room_preference = request.POST.get(
            "room_preference"
        )
        reason = request.POST.get("reason")

        hostel = get_object_or_404(
            Hostel,
            id=hostel_id
        )

        # Check whether the selected room type
        # actually has an available bed
        available_beds = Bed.objects.filter(
            room__hostel=hostel,
            room__sharing_type=room_preference,
            is_booked=False
        ).count()

        if available_beds == 0:

            messages.error(
                request,
                "No beds are currently available for this room preference."
            )

            return redirect("apply_hostel")

        HostelApplication.objects.create(
            student=request.user,
            hostel=hostel,
            room_preference=room_preference,
            reason=reason
        )

        messages.success(
            request,
            "Your hostel application has been submitted."
        )

        return redirect("my_application")

    return render(
        request,
        "apply_hostel.html",
        {
            "hostels": hostels
        }
    )
@login_required
def my_application(request):

    application = HostelApplication.objects.filter(
        student=request.user
    ).order_by("-applied_at").first()

    return render(
        request,
        "my_application.html",
        {
            "application": application
        }
    )

@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return HttpResponse(
            "You are not authorized to access this page."
        )

    from django.contrib.auth.models import User

    total_students = User.objects.filter(
        is_staff=False
    ).count()

    total_hostels = Hostel.objects.count()
    total_rooms = Room.objects.count()
    total_beds = Bed.objects.count()

    available_beds = Bed.objects.filter(
        is_booked=False
    ).count()

    pending_applications = HostelApplication.objects.filter(
        status="Pending"
    ).count()

    # Hostel-wise availability
    hostels = Hostel.objects.all()

    for hostel in hostels:

        hostel.room_count = Room.objects.filter(
            hostel=hostel
        ).count()

        hostel.total_beds_count = Bed.objects.filter(
            room__hostel=hostel
        ).count()

        hostel.available_beds_count = Bed.objects.filter(
            room__hostel=hostel,
            is_booked=False
        ).count()

    context = {
        "total_students": total_students,
        "total_hostels": total_hostels,
        "total_rooms": total_rooms,
        "total_beds": total_beds,
        "available_beds": available_beds,
        "pending_applications": pending_applications,
        "hostels": hostels,
    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )
@login_required
def admin_applications(request):

    if not request.user.is_staff:
        return HttpResponse(
            "You are not authorized to access this page."
        )

    applications = HostelApplication.objects.select_related(
        "student",
        "hostel"
    ).order_by("-applied_at")

    for application in applications:

        application.available_beds_count = Bed.objects.filter(
            room__hostel=application.hostel,
            room__sharing_type=application.room_preference,
            is_booked=False
        ).count()

    return render(
        request,
        "admin_applications.html",
        {
            "applications": applications
        }
    )
@login_required
def approve_application(request, application_id):

    if not request.user.is_staff:
        return HttpResponse(
            "Unauthorized"
        )

    application = get_object_or_404(
        HostelApplication,
        id=application_id
    )

    # 1. Application must still be pending
    if application.status != "Pending":

        messages.warning(
            request,
            "This application has already been processed."
        )

        return redirect("admin_applications")

    # 2. Student must not already have an allocation
    if Booking.objects.filter(
        student=application.student
    ).exists():

        messages.warning(
            request,
            "This student already has an allocation."
        )

        return redirect("admin_applications")

    # 3. Find rooms matching:
    #    - selected hostel
    #    - selected sharing preference
    #    - at least one available bed
    available_rooms = Room.objects.filter(
        hostel=application.hostel,
        sharing_type=application.room_preference,
        beds__is_booked=False
    ).distinct()

    if not available_rooms.exists():

        messages.error(
            request,
            "No suitable room or bed is currently available."
        )

        return redirect("admin_applications")

    # 4. Select the room with the most available beds
    selected_room = max(
        available_rooms,
        key=lambda room: room.available_beds
    )

    # 5. Get an available bed from that room
    available_bed = selected_room.beds.filter(
        is_booked=False
    ).first()

    if not available_bed:

        messages.error(
            request,
            "No available bed found in the selected room."
        )

        return redirect("admin_applications")

    # 6. Mark the bed as booked
    available_bed.is_booked = True
    available_bed.save()

    # 7. Create the student's booking
    Booking.objects.create(
        student=application.student,
        bed=available_bed
    )

    # 8. Approve the application
    application.status = "Approved"
    application.save()

    messages.success(
        request,
        f"Application approved for {application.student.username}."
    )

    return redirect("admin_applications")

@login_required
def reject_application(request, application_id):

    if not request.user.is_staff:
        return HttpResponse(
            "Unauthorized"
        )

    application = get_object_or_404(
        HostelApplication,
        id=application_id
    )
    

    application.status = "Rejected"
    application.save()

    messages.info(
        request,
        "Application rejected."
    )

    return redirect("admin_applications")
@login_required
def admin_hostel_detail(request, hostel_id):

    if not request.user.is_staff:
        return HttpResponse(
            "You are not authorized to access this page."
        )

    hostel = get_object_or_404(
        Hostel,
        id=hostel_id
    )

    rooms = Room.objects.filter(
        hostel=hostel
    ).prefetch_related("beds")

    return render(
        request,
        "admin_hostel_detail.html",
        {
            "hostel": hostel,
            "rooms": rooms
        }
    )
@login_required
def admin_hostel_detail(request, hostel_id):

    if not request.user.is_staff:
        return HttpResponse(
            "You are not authorized to access this page."
        )

    hostel = get_object_or_404(
        Hostel,
        id=hostel_id
    )

    rooms = Room.objects.filter(
        hostel=hostel
    ).prefetch_related("beds")

    return render(
        request,
        "admin_hostel_detail.html",
        {
            "hostel": hostel,
            "rooms": rooms
        }
    )