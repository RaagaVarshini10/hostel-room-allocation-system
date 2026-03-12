from django.urls import path
from . import views

urlpatterns = [
    path('hostels/', views.hostel_list, name='hostel_list'),
    path('hostel/<int:hostel_id>/', views.hostel_detail, name='hostel_detail'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('book/<int:bed_id>/', views.book_bed, name='book_bed'),
    path('my-booking/', views.my_booking, name='my_booking'),
]
