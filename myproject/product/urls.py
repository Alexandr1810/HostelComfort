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
    
    #frontend
    path('hotel/', views.hotel_1, name = 'hotel_1'),
    path('hotel_frontend/', views.hotel_detail, name='hotel_detail_1'),
    path('booking_frontend/', views.booking_1, name = 'booking_1'),
    path('booking_info_frontend/', views.booking_info_1, name = 'booking_info_1'),
    path('login_frontend/', views.user_login_1, name = 'login_1'),
    path('logout_frontend/', views.user_logout_1, name='user_login_1'),
    path('register_frontend/', views.register_1, name = 'register_1'),
    path('profile_frontend/', views.user_profile_1, name = 'user_profile_1'),
]