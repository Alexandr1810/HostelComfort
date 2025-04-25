from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel, name='hotel'),
    path('hotel/<int:id>/', views.hotel_detail, name='hotel_detail'),
    path('booking/<int:id>/', views.booking, name='booking'),
    path('booking_info/<int:id>/', views.booking_info, name='booking_info'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='user_profile'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
