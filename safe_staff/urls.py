from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from safe_staff import views
from django.urls import include # type: ignore
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.staff_login, name='staff_login'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('staff_home/', views.staff_home, name='staff_home'),
    path('staff_userver/', views.staff_userver, name='staff_userver'),
    path('staff_veic/', views.staff_veic, name='staff_veic'),
    path('staff_ord/', views.staff_ord, name='staff_ord'),
    path('staff_logout/', views.staff_logout, name='staff_logout'),
    path('staff_user/',views.staff_user,name='staff_user'),
    
    path('staff_book/',views.staff_book,name='staff_book'),
    path('staff_ser/',views.staff_ser,name='staff_ser'),
    path('staff_logout/',views.staff_logout,name='staff_logout'),
    path('staff_update_user_price/<int:book_id>/',views.staff_update_user_price,name='staff_update_user_price'),
    path('staff_update_user_book_status/<int:book_id>/',views.staff_update_user_book_status,name='staff_update_user_book_status'),
    path('user_verify/<int:user_id>/',views.user_verify,name='user_verify'),
    path('staff_vehicle_edit/<veic_id>',views.staff_vehicle_edit,name='staff_vehicle_edit'),
    path('edit_user/<int:user_id>/',views.edit_user,name='edit_user'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
