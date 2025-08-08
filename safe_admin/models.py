from turtle import up
from django.db import models # type: ignore
import os
from datetime import datetime,date,time
from django.utils import timezone


# Custom upload path for vehicle images using license_plate and current date
def vehicle_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    license_plate = instance.license_plate.replace(' ', '_') if instance.license_plate else 'unknown'
    return os.path.join('vic_pic', f"{license_plate}_{now}.{ext}")

# Custom upload path for user addhar image
def user_addhar_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    return os.path.join('user_addhar', f"user_{instance.id}_addhar_{now}.{ext}")

# Custom upload path for user dl image
def user_dl_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    return os.path.join('user_dl', f"user_{instance.id}_dl_{now}.{ext}")

def user_city_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    return os.path.join('city_pic', f"city_{instance.id}_city_{now}.{ext}")
def user_staff_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    return os.path.join('staff_pic', f"staff_{instance.id}_staff_{now}.{ext}")
def user_profile_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    return os.path.join('profile_pic_user', f"profile_{instance.id}_profile_{now}.{ext}")




def conferm_booking(request, city):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            user_obj = Users.objects.get(phone_number=user.username)
            # ...existing code...
            now_str = datetime.now().strftime('%Y%m%d%H%M%S')
            booking_id = f"{user_obj.id}_{now_str}"
            # Pass booking_id to your Booking model or context
# Create your models here.

# 1. Users
class Users(models.Model):
    id= models.AutoField(primary_key=True)
    user_profile_image = models.ImageField(upload_to=user_profile_image_upload_path, blank=True, null=True)
    user_gender = models.CharField(max_length=20)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    driver_license_number = models.CharField(max_length=255)
    addhar_number = models.CharField(max_length=255)
    user_addhar_image=models.ImageField(upload_to=user_addhar_image_upload_path, blank=True, null=True)
    user_dl_image=models.ImageField(upload_to=user_dl_image_upload_path, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at= models.DateTimeField(auto_now=True)
    
    DisplayFields=[
        'id', 'first_name', 'user_profile_image', 'last_name', 'email', 'password_hash', 'phone_number',
        'driver_license_number', 'addhar_number', 'user_addhar_image', 'user_dl_image',
        'address', 'created_at', 'edited_at', 'is_active', 'is_verified'
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# 2. Locations
class Location(models.Model):
    
    
    id= models.AutoField(primary_key=True)
    city = models.CharField(max_length=255)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    Location_image=models.ImageField(upload_to=user_city_image_upload_path,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    edited_at= models.DateTimeField(auto_now=True,blank=True,null=True)
    DisplayFields=[
        'id', 'city', 'address', 'pincode', 'Location_image', 'is_active','created_at','edited_at'
    ]
    def __str__(self):
        return f"{self.city} - {self.address}"

# 3. vehicle Categories
class vehicleCategory(models.Model):
    
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    edited_at= models.DateTimeField(auto_now=True,blank=True,null=True)
    DisplayFields=[
        'id', 'name', 'description'
    ]
    def __str__(self):
        return self.name

# 4. vehicles
class vehicle(models.Model):
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Maintenance'),
    ]
    
    id= models.AutoField(primary_key=True)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    vehicle_image = models.ImageField(upload_to=vehicle_image_upload_path, blank=True, null=True)
    category = models.ForeignKey(vehicleCategory, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    hourly_rate_wo_driver = models.DecimalField(max_digits=10, decimal_places=2)
    hourly_rate_with_driver = models.DecimalField(max_digits=10, decimal_places=2)
    daily_rate_wo_driver = models.DecimalField(max_digits=10, decimal_places=2)
    daily_rate_with_driver = models.DecimalField(max_digits=10, decimal_places=2)
    weekly_rate_wo_driver = models.DecimalField(max_digits=10, decimal_places=2)
    weekly_rate_with_driver = models.DecimalField(max_digits=10, decimal_places=2)
    fif_day_rate_wo_driver = models.DecimalField(max_digits=10, decimal_places=2)
    fif_day_rate_with_driver = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_rate_wo_driver = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_rate_with_driver = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    allot_city = models.CharField(max_length=100)
    last_eddit_by = models.CharField(max_length=255, blank=True, null=True)  # New field to track last editor
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    edited_at= models.DateTimeField(auto_now=True,blank=True,null=True)
    DisplayFields=[
        'id', 'make', 'model', 'year', 'license_plate', 'vehicle_image', 'category',
        'location','last_eddit_by', 'hourly_rate_wo_driver', 'hourly_rate_with_driver', 'daily_rate_wo_driver', 
        'daily_rate_with_driver', 'weekly_rate_wo_driver', 'weekly_rate_with_driver', 
        'fif_day_rate_wo_driver', 'fif_day_rate_with_driver', 'monthly_rate_wo_driver', 
        'monthly_rate_with_driver', 'status', 'allot_city',
    ]
    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

# 5. Bookings
class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    booking_number = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)  # Allow null for bookings without a user
    vehicle = models.ForeignKey(vehicle, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    pickup_location_id = models.CharField(max_length=30, null=True, blank=True)
    dropoff_location_id = models.CharField(max_length=30, null=True, blank=True)
    driver_choice = models.CharField(max_length=20, default='self_drive' , null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    user_price = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2)
    booking_status = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    last_edited_by_book_price = models.CharField(max_length=255, blank=True, null=True)  # New field to track last editor
    last_edited_by_book_status = models.CharField(max_length=255, blank=True, null=True)  # New field to track last editor

    DisplayFields = [
        'id', 'booking_number', 'user', 'vehicle', 'start_time', 'end_time', 'pickup_location_id',
        'dropoff_location_id', 'total_price', 'booking_status','user_price', 'created_at', 
        'edited_at','last_edited_by_book_price','last_edited_by_book_status'
    ]
    def __str__(self):
        return f"Booking #{self.id} - {self.user}"

# 6. Payments
class Payment(models.Model):
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    id= models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    edited_at= models.DateTimeField(auto_now=True,blank=True,null=True)
    DisplayFields=[
        'id', 'booking', 'amount', 'payment_method', 'transaction_id', 'payment_status'
    ]
    def __str__(self):
        return f"Payment #{self.id} - {self.amount}"

# 7. Reviews
class Review(models.Model):
    
    id= models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(vehicle, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    edited_at= models.DateTimeField(auto_now=True,blank=True,null=True)
    DisplayFields=[
        'id', 'user', 'vehicle', 'booking', 'rating', 'comment',
    ]
    def __str__(self):
        return f"Review #{self.id} by {self.user.email}"


class Marketing_model(models.Model):
    id=models.AutoField(primary_key=True)
    Marketing_email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    edited_at= models.DateTimeField(auto_now=True,blank=True,null=True)
    DisplayFields=[
        'id','Marketing_email','created_at','edited_at'
    ]
    def __str__(self):
        return self.Marketing_email
    

class ServicesDetail(models.Model):
    
    Pick_drop_choice = [
        ('pickup', 'pickup'),
        ('drop', 'drop'),
    ]
    id= models.AutoField(primary_key=True)
    vehicle_id=models.ForeignKey(vehicle,on_delete=models.CASCADE,related_name='pickup_drop_bookings')
    user_id=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='user_pickup_drop_bookings')
    address_of_origin=models.TextField(max_length=300,null=False)
    picl_drop=models.CharField(max_length=30,choices=Pick_drop_choice)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    edited_at= models.DateTimeField(auto_now=True,blank=True,null=True)
    DisplayFields=[
        'id', 'vehicle_id', 'user_id', 'address_of_origin', 'picl_drop'
    ]
    def __str__(self):
        return self.ServicesDetail

class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    area= models.CharField(max_length=255)
    area_forigen= models.ForeignKey(Location,on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    image= models.ImageField(upload_to=user_staff_image_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    DisplayFields = [
        'id', 'full_name', 'username', 'password_hash', 'email', 'phone_number', 'created_at', 'edited_at','is_active', 'is_staff', 'image'
    ]

    def __str__(self):
        return self.username
    
class PhoneOTP(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    DisplayFields = [
        'phone', 'otp', 'is_verified', 'created_at'
    ]
    def __str__(self):
        return f"OTP for {self.phone} - {self.otp}"
    

class contact_form_user(models.Model):
    id = models.AutoField(primary_key=True)
    contact_name_page=models.TextField(max_length=30)
    contact_email=models.EmailField(max_length=50)
    messege=models.TextField()
    if_username=models.TextField(max_length=30)
    DisplayFields=[
        'id','contact_email','messege','if_username'
    ]

