from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel, name='hotel'),
    path('hotel/<int:id>/', views.hotel_info, name='hotel_info'),
    path('booking/<int:id>/', views.booking, name='booking'),
    path('booking/<int:id>/<int:room_number>/', views.booking, name='booking'),
    path('booking_info/<int:id>/', views.booking_info, name='booking_info'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='user_profile'),
    path('hotel_manager/', views.hotel_manager, name='hotel_manager'),
    path('add/', views.add, name='add'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('comment_delete/<int:id>/', views.comment_delete, name='comment_delete'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('hotel/<int:hotel_id>/room/<int:room_number>/edit/', views.edit_room, name='edit_room'),
]
