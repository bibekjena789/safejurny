from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from safe_user import views
from django.urls import include # type: ignore
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from safejurny import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('city_home', views.city_home, name='city_home'),
    path('home_about', views.home_about, name='home_about'),
    path('user_tariff', views.user_tariff, name='user_tariff'),
    path('filter_taxi', views.filter_taxi, name='filter_taxi'),
    path('filter_car', views.filter_car, name='filter_car'),
    path('user_fecility', views.user_fecility, name='user_fecility'),
    path('user_filter_facility', views.user_filter_facility, name='user_filter_facility'),
    path('user_filter', views.user_filter, name='user_filter'),
    path('user_bookings', views.user_bookings, name='user_bookings'),
    
    
    path('user_profile', views.user_profile, name='user_profile'),
    path('confirm_booking', views.confirm_booking, name='confirm_booking'),
    path('<str:city>/user_update_detail', views.user_update_detail, name='user_update_detail'),
    path('user_login', views.user_login, name='user_login'),
    path('user_signup', views.user_signup, name='user_signup'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_contact', views.user_contact, name='user_contact'),
    path('user_update_detail', views.user_update_detail, name='user_update_detail'),
    path('send_otp', views.send_otp, name='send_otp'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('reset_pass', views.reset_pass, name='reset_pass'),
    
    #path('city_home', views.city_home, name='city_home'),
    path('marketing_emails', views.marketing_emails, name='marketing_emails'),
    path('<str:city>/bike-rentals/', views.city_bike_rentals, name='city_bike_rentals'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path('<str:city>/user_filter_book/<int:vkl_id>/', views.user_filter_book, name='user_filter_book')
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
