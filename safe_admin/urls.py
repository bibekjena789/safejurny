
from django.urls import path 
from safe_staff import views
from safe_admin import views
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    #path('admin_users/', views.admin_users, name='admin_users'),
    #path('admin_vehicle_category/', views.admin_vehicle_category, name='admin_vehicle_category'),
    #path('admin_vehicle_list/', views.admin_vehicle_list, name='admin_vehicle_list'),
    #path('admin_vehicle_create/', views.admin_vehicle_create, name='admin_vehicle_create'),
    #path('admin_vehicle_edit/<int:vehicle_id>/', views.admin_vehicle_edit, name='admin_vehicle_edit'),
    #path('admin_vehicle_delete/<int:vehicle_id>/', views.admin_vehicle_delete, name='admin_vehicle_delete'),
    #path('admin_booking_list/', views.admin_booking_list, name='admin_booking_list'),
    #path('admin_booking_detail/<int:booking_id>/', views.admin_booking_detail, name='admin_booking_detail'),
    #path('admin_booking_edit/<int:booking_id>/', views.admin_booking_edit, name='admin_booking_edit'),
    #path('admin_booking_delete/<int:booking_id>/', views.admin_booking_delete, name='admin_booking_delete'),
    #path('admin_payment_create/', views.admin_payment_create, name='admin_payment_create'),
    #path('admin_payment_edit/<int:payment_id>/', views.admin_payment_edit, name='admin_payment_edit'),
    #path('admin_payment_delete/<int:payment_id>/', views.admin_payment_delete, name='admin_payment_delete'),
    #path('admin_review_list/', views.admin_review_list, name='admin_review_list'),  
    path('admin_payment_list/', views.admin_payment_list, name='admin_payment_list'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
