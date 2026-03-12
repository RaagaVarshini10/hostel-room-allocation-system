from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Hostel,Room,Bed,Booking
from django.shortcuts import redirect

def hostel_list(request):
    hostels = Hostel.objects.all()
    return render(request, 'hostel_list.html', {'hostels': hostels})
def hostel_detail(request, hostel_id):
    hostel = Hostel.objects.get(id=hostel_id)
    rooms = Room.objects.filter(hostel=hostel)
    return render(request, 'hostel_detail.html', {
        'hostel': hostel,
        'rooms': rooms
    })
def room_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    beds = Bed.objects.filter(room=room)
    return render(request, 'room_detail.html', {
        'room': room,
        'beds': beds
    })
@login_required
def book_bed(request, bed_id):
    bed = Bed.objects.get(id=bed_id)

    # If bed already booked
    if bed.is_booked:
        return HttpResponse("This bed is already booked.")

    # If user already booked a bed
    if Booking.objects.filter(student=request.user).exists():
        return HttpResponse("You already booked a bed.")

    bed.is_booked = True
    bed.save()

    Booking.objects.create(
        student=request.user,
        bed=bed
    )

    return redirect('my_booking')

@login_required
def my_booking(request):
    booking = Booking.objects.filter(student=request.user).first()
    return render(request, 'my_booking.html', {
        'booking': booking
    })
