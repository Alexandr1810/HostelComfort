from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.hotel, name = 'hotel'),
    path('hotel_info/<int:id>/', views.hotel_info, name='hotel_info'),
    path('booking/<int:id>/', views.booking, name = 'booking'),
    path('booking_info/<int:id>/', views.booking_info, name = 'booking_info'),
    path('login/', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('profile/', views.profile, name = 'profile'),
    
    #frontend
    path('hotel/', views.hotel_1, name = 'hotel_1'),
    path('hotel_info_frontend/', views.hotel_info_1, name='hotel_info_1'),
    path('booking_frontend/', views.booking_1, name = 'booking_1'),
    path('booking_info_frontend/', views.booking_info_1, name = 'booking_info_1'),
    path('login_frontend/', views.login_1, name = 'login_1'),
    path('register_frontend/', views.register_1, name = 'register_1'),
    path('profile_frontend/', views.profile_1, name = 'profile_1'),
=======
    path('', views.hotel, name='hotel'),
    path('hotel/<int:id>/', views.hotel_detail, name='hotel_detail'),
    path('booking/<int:id>/', views.booking, name='booking'),
    path('booking_info/<int:id>/', views.booking_info, name='booking_info'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='user_profile'),
>>>>>>> ec21fd3f5b4b67e386a4fb090478e03e638ca386
]