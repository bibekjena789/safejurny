from django.contrib import admin  # type: ignore
from .models import (
                      Staff, Users,Location,vehicleCategory,vehicle,
                      Booking,Payment,Review,Marketing_model,ServicesDetail,
                      PhoneOTP,contact_form_user
                    )

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = Users.DisplayFields
    search_fields = ('first_name', 'last_name', 'email', 'phone_number','addhar_number')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = Location.DisplayFields
    list_filter = ('is_active', 'city')
    search_fields = ('city', 'pincode')

@admin.register(vehicleCategory)
class vehicleCategoryAdmin(admin.ModelAdmin):
    list_display = vehicleCategory.DisplayFields
    search_fields = ('name',)

@admin.register(vehicle)
class vehicleAdmin(admin.ModelAdmin):
    list_display = vehicle.DisplayFields
    list_filter = ('status', 'category', 'location')
    search_fields = ('make', 'model', 'license_plate')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = Booking.DisplayFields
    list_filter = ('booking_status', 'driver_choice')
    search_fields = ('booking_number', 'user__email', 'vehicle__model', 'pickup_location_id', 'dropoff_location_id')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = Payment.DisplayFields
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('transaction_id',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = Review.DisplayFields
    search_fields = ('user__email', 'vehicle__model')

    
@admin.register(Marketing_model)
class Marketing_modelAdmin(admin.ModelAdmin):
    list_display = Marketing_model.DisplayFields
    search_fields = ('Marketing_email','subscribed_at')

@admin.register(ServicesDetail)
class ServicesDetailAdmin(admin.ModelAdmin):
    list_display = ServicesDetail.DisplayFields
    search_fields = ('id','vehicle_id','user_id','address_of_origin','picl_drop')
    
@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = PhoneOTP.DisplayFields
    

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = Staff.DisplayFields
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('is_active', 'is_staff')
@admin.register(contact_form_user)
class contact_form_userAdmin(admin.ModelAdmin):
    list_display = contact_form_user.DisplayFields
    search_fields = ('id','contact_email','messege','if_username')
    list_filter = ('id','contact_email','messege','if_username')
    

