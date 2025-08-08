from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from safe_admin.models import (
                      Staff, Users,Location,vehicleCategory,vehicle,
                      Booking,Payment,Review,Marketing_model,ServicesDetail,
                      PhoneOTP,contact_form_user
                    )
import os, time, random, string, logging
from captcha.image import ImageCaptcha
from decimal import Decimal, InvalidOperation








def to_decimal(value, default):
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return default




def staff_required(view_func=None, login_url=None):
    """
    Decorator for views that checks that the user is logged in and is a staff member.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
# Create your views here.



def staff_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('staff_home')
    if request.method == 'POST':
        username = request.POST.get('staff_username', '').strip()
        password = request.POST.get('staff_password', '').strip()
        user = authenticate(username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('staff_home')
        else:
            return render(request, 'staff/staff_login.html', {'error': 'Invalid credentials'})
    return render(request, 'staff/staff_login.html')




def staff_logout(request):
    logout(request)
    return redirect('staff_login')

@staff_required(login_url='staff_login')
def staff_home(request):
    staff_data= Staff.objects.filter(username=request.user.username).first()
    if not staff_data:
        return HttpResponse("Staff data not found", status=404)
    bike_list = vehicle.objects.filter(category__name__iexact='BIKE', location=staff_data.area_forigen).all()
    car_list = vehicle.objects.filter(category__name__iexact='CAR', location=staff_data.area_forigen).all()
    scooty_list = vehicle.objects.filter(category__name__iexact='Scooty', location=staff_data.area_forigen).all()
    context = {
        'staff_data': staff_data,
        'staff': request.user,
        'bike_list': bike_list,
        'car_list' : car_list,
        'scooty_list': scooty_list,
    }
    return render(request, 'staff/staff_home.html', context)

@staff_required(login_url='staff_login')
def staff_userver(request):
    staff_data= Staff.objects.filter(username=request.user.username).first()
    if not staff_data:
        return HttpResponse("Staff data not found", status=404)
    if request.method == 'GET':
        search_query = request.GET.get('search', '').strip()
        if search_query:
            all_user = Users.objects.filter(first_name__icontains=search_query).all().order_by('-created_at')
            tobe_verify = Users.objects.filter(is_verified=0, first_name__icontains=search_query).all().order_by('-created_at')
            verified = Users.objects.filter(is_verified=1, first_name__icontains=search_query).all().order_by('-created_at')
        else:
            all_user = Users.objects.all() .order_by('-created_at')
            tobe_verify = Users.objects.filter(is_verified=0).all().order_by('-created_at')
            verified = Users.objects.filter(is_verified=1).all().order_by('-created_at')
        context = {
            'staff_data': staff_data,
            'staff': request.user,
            'all_user': all_user,
            'tobe_verify': tobe_verify,
            'verified': verified,
        }
    else:
        all_user = Users.objects.all().order_by('-created_at')
        tobe_verify = Users.objects.filter(is_verified=0).all().order_by('-created_at')
        verified = Users.objects.filter(is_verified=1).all().order_by('-created_at')
        context = {
            'staff_data': staff_data,
            'staff': request.user,
            'all_user': all_user,
            'tobe_verify': tobe_verify,
            'verified': verified,
        }
    return render(request, 'staff/staff_very.html', context)
@staff_required(login_url='staff_login')
def user_verify(request, user_id):
    user = Users.objects.get(id=user_id)
    if user:
        user.is_verified = True
        user.save()
        return redirect('staff_userver')
    else:
        return HttpResponse("User not found", status=404)
@staff_required(login_url='staff_login')
def edit_user(request, user_id):
    staff_data= Staff.objects.filter(username=request.user.username).first()
    user_data= Users.objects.filter(id=user_id).first()
    if request.method == 'POST':
        user_image = request.FILES.get('profile_img')
        user_gender = request.POST.get('user_gender', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        driver_license_number = request.POST.get('driver_license_number', '').strip()
        addhar_number = request.POST.get('addhar_number', '').strip()
        dl_image = request.FILES.get('drivers_license_image')
        adhar_image = request.FILES.get('addhar_image')
        address = request.POST.get('address', '').strip()
        if user_data:
            user_data.user_profile_image = user_image if user_image else user_data.user_profile_image
            user_data.user_gender = user_gender if user_gender else user_data.user_gender
            user_data.first_name = first_name if first_name else user_data.first_name
            user_data.last_name = last_name if last_name else user_data.last_name
            user_data.email = email if email else user_data.email
            user_data.phone_number = phone if phone else user_data.phone_number
            user_data.driver_license_number = driver_license_number if driver_license_number else user_data.driver_license_number
            user_data.addhar_number = addhar_number if addhar_number else user_data.addhar_number
            user_data.user_dl_image = dl_image if dl_image else user_data.user_dl_image
            user_data.user_addhar_image = adhar_image if adhar_image else user_data.user_addhar_image
            user_data.is_verified = True  # Assuming you want to mark as verified after edit
            user_data.is_active = True  # Assuming you want to keep the user active
            user_data.address = address if address else user_data.address
            user_data.save()
            return redirect('staff_userver')
        else:
            return HttpResponse("User not found", status=404)
    context = {
        'staff_data': staff_data,
        'staff': request.user,
        'user_data': user_data,
    }
    return render(request, 'staff/staff_userss_form.html', context)

@staff_required(login_url='staff_login')
def staff_veic(request):
    staff_data= Staff.objects.filter(username=request.user.username).first()
    if not staff_data:
        return HttpResponse("Staff data not found", status=404)
    bike_list = vehicle.objects.filter(category__name='BIKE', location=staff_data.area_forigen).all()
    car_list = vehicle.objects.filter(category__name='CAR', location=staff_data.area_forigen).all()
    scooty_list = vehicle.objects.filter(category__name='Scooty', location=staff_data.area_forigen).all()
    context = {
        'staff_data': staff_data,
        'staff': request.user,
        'bike_list': bike_list,
        'car_list' : car_list,
        'scooty_list': scooty_list,
    }
    return render(request, 'staff/staff_manage_vic.html',context)
@staff_required(login_url='staff_login')
def staff_ord(request):
    staff_data= Staff.objects.filter(username=request.user.username).first()
    if not staff_data:
        return HttpResponse("Staff data not found", status=404)
    book_data= Booking.objects.filter().all().order_by('-created_at')
    context={
        'book_data':book_data,
        'staff_data': staff_data,
        'staff': request.user,
    }

    return render(request, 'staff/staff_order.html', context)

@staff_required(login_url='staff_login')
def staff_update_user_price(request, book_id):
    if request.method == 'POST':
        new_price = request.POST.get('new_price', '').strip()
        last_edited_by = request.user.username if request.user.is_authenticated else 'Unknown'
        try:
            book = Booking.objects.get(id=book_id)
            book.user_price = new_price
            book.last_edited_by_book_price = last_edited_by
            book.save()
        except Booking.DoesNotExist:
            return HttpResponse("Booking not found", status=404)
        return redirect('staff_ord')
    
    
@staff_required(login_url='staff_login')
def staff_update_user_book_status(request, book_id):
    if request.method == 'POST':
        new_status = request.POST.get('new_status', '').strip()
        last_updated_by = request.user.username if request.user.is_authenticated else 'Unknown'
        try:
            book = Booking.objects.get(id=book_id)
            book.booking_status = new_status
            book.last_edited_by_book_status = last_updated_by
            book.save()
        except Booking.DoesNotExist:
            return HttpResponse("Booking not found", status=404)
        return redirect('staff_ord')



@staff_required(login_url='staff_login')
def staff_user(request):
    staff_data= Staff.objects.filter(username=request.user.username).first()
    if not staff_data:
        return HttpResponse("Staff data not found", status=404)
    context={
        'staff_data': staff_data,
        'staff': request.user,
    }
    return render(request, 'staff/staff_userss_form.html', context)

@staff_required(login_url='staff_login')
def staff_vehicle_edit(request,veic_id):
    staff_data= Staff.objects.filter(username=request.user.username).first()
    filtered_vehicle = vehicle.objects.filter(id=veic_id).first()
    if not staff_data:
        return HttpResponse("Staff data not found", status=404)
    
    if request.method == 'POST':
        hourly_with_driver = request.POST.get('hourly_with_driver', '').strip()
        hourly_without_driver = request.POST.get('hourly_wo_driver', '').strip()
        daily_with_driver = request.POST.get('daily_with_driver', '').strip()   
        daily_without_driver = request.POST.get('daily_wo_driver', '').strip()
        weekly_with_driver = request.POST.get('weekly_with_driver', '').strip()
        weekly_without_driver = request.POST.get('weekly_wo_driver', '').strip()
        half_monthly_with_driver = request.POST.get('fifteen_day_with_driver', '').strip()
        half_monthly_without_driver = request.POST.get('fifteen_day_wo_driver', '').strip()
        monthly_with_driver = request.POST.get('monthly_with_driver', '').strip()
        monthly_without_driver = request.POST.get('monthly_wo_driver', '').strip()
        last_eddit_by = request.user.username  # Track who last edited the vehicle
        vkl_status = request.POST.get('status', '').strip()
        if filtered_vehicle:
            filtered_vehicle.hourly_rate_wo_driver = hourly_without_driver if hourly_without_driver else filtered_vehicle.hourly_rate_wo_driver
            filtered_vehicle.hourly_rate_with_driver = hourly_with_driver if hourly_with_driver else filtered_vehicle.hourly_rate_with_driver
            filtered_vehicle.daily_rate_wo_driver = daily_without_driver if daily_without_driver else filtered_vehicle.daily_rate_wo_driver
            filtered_vehicle.daily_rate_with_driver = daily_with_driver if daily_with_driver else filtered_vehicle.daily_rate_with_driver
            filtered_vehicle.weekly_rate_with_driver = weekly_with_driver if weekly_with_driver else filtered_vehicle.weekly_rate_with_driver
            filtered_vehicle.weekly_rate_wo_driver = weekly_without_driver if weekly_without_driver else filtered_vehicle.weekly_rate_wo_driver
            filtered_vehicle.fif_day_rate_with_driver = half_monthly_with_driver if half_monthly_with_driver else filtered_vehicle.fif_day_rate_with_driver
            filtered_vehicle.fif_day_rate_wo_driver = half_monthly_without_driver if half_monthly_without_driver else filtered_vehicle.fif_day_rate_wo_driver
            filtered_vehicle.monthly_rate_with_driver = monthly_with_driver if monthly_with_driver else filtered_vehicle.monthly_rate_with_driver
            filtered_vehicle.monthly_rate_wo_driver = monthly_without_driver if monthly_without_driver else filtered_vehicle.monthly_rate_wo_driver
            filtered_vehicle.status = vkl_status if vkl_status else filtered_vehicle.status
            filtered_vehicle.last_eddit_by = last_eddit_by if last_eddit_by else filtered_vehicle.last_eddit_by
            filtered_vehicle.save()
            return redirect('staff_veic')
    context={
        'staff_data': staff_data,
        'staff': request.user,
        'filtered_vehicle': filtered_vehicle,
    }
    return render(request, 'staff/staff_vehicle_form.html', context)


@staff_required(login_url='staff_login')
def staff_book(request):
    staff_data= Staff.objects.filter(username=request.user.username).first()
    if not staff_data:
        return HttpResponse("Staff data not found", status=404)
    context={
        'staff_data': staff_data,
        'staff': request.user,
    }
    return render(request, 'staff/staff_booking.html', context)



@staff_required(login_url='staff_login')
def staff_ser(request):
    staff_data= Staff.objects.filter(username=request.user.username).first()
    if not staff_data:
        return HttpResponse("Staff data not found", status=404)
    
    context={
        'staff_data': staff_data,
        'staff': request.user,
    }
    return render(request, 'staff/staff_service_form.html', context)

