from django.shortcuts import render # type: ignore
from safe_admin.models import Location, Marketing_model, Users,vehicle,PhoneOTP,contact_form_user,Booking
#from django.shortcuts import redirect, get_list_or_404, get_object_or_404
from django.shortcuts import redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, get_user
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .utils import generate_otp, send_otp_via_whatsapp, generate_captcha
from PIL import Image, ImageDraw, ImageFont
from django.core.mail import send_mail

# Create your views here.

#LOGIN_URL = '/user_login/'

def index(request, city=None):
    operation_location= Location.objects.all()
    
    context = {
        'city':city,
        'operation_location': operation_location,
    }
    return render(request, 'pages/index.html',context)



def home_about(request, city):
    location = city.lower()
    filter_vkl = vehicle.objects.filter(allot_city=location).all()
    operation_location= Location.objects.all()
    context = {
        'city': city.capitalize(),
        'location': location,
        'filter_vkl': filter_vkl,
        'operation_location': operation_location,
    }
    return render(request, 'pages/cli_about.html', context)



def city_home(request, city):
    location = city.lower()
    filter_vkl = vehicle.objects.filter(allot_city=location).all()
    operation_location= Location.objects.all()
    context = {
        'city': city.capitalize(),
        'location': location,
        'filter_vkl': filter_vkl,
        'operation_location': operation_location,
    }
    
    
    return render(request, 'pages/filter_city_temp.html', context)
def user_contact(request, city):
    location = city.lower()
    filter_vkl = vehicle.objects.filter(allot_city=location).all()
    operation_location= Location.objects.all()
    session_username = request.session.get('username')
    if request.method == 'POST':
        pers_name = request.POST.get('name')
        pers_email = request.POST.get('email')
        pers_messege = request.POST.get('message')
        pers_session_user = session_username if session_username else pers_name if pers_name else 'Anonymous'

        update_contact = contact_form_user(
            contact_email=pers_email,
            messege=pers_messege,
            contact_name_page=pers_name,
            if_username=pers_session_user
        )
        send_mail(
             subject='Noreplay',
             message=f'Hello,{pers_name}, \n\t We will contact you very soon.\n\t Your contact E-mail is {pers_email}.\n\t Your messege is {pers_messege}',
             from_email='safejourney9090@gmail.com',  # Replace with your email
             recipient_list=[pers_email],
             fail_silently=False,
             
                )

        update_contact.save()

    
    context = {
        'city': city.capitalize(),
        'location': location,
        'filter_vkl': filter_vkl,
        'operation_location': operation_location,
        'session_username': session_username,
    }
    return render(request, 'pages/user_contact.html', context)
def user_fecility(request, city):
    location = city.lower()
    filter_vkl = vehicle.objects.filter(allot_city=location).all()
    operation_location= Location.objects.all()
    context = {
        'city': city.capitalize(),
        'location': location,
        'filter_vkl': filter_vkl,
        'operation_location': operation_location,
    }
    
    return render(request, 'pages/user_facilities.html', context)

def user_tariff(request,city):
    location = city.lower()
    filter_vkl = vehicle.objects.filter(allot_city=location).all()
    operation_location= Location.objects.all()
    vkl_name='Bikes & Cars'
    if not filter_vkl:
        raise Http404("No vehicles available in this city.")
    context = {
        'vkl_name':vkl_name,
        'city': city.capitalize(),
        'location': location,
        'filter_vkl': filter_vkl,
        'operation_location': operation_location,
    }
    return render(request, 'pages/filter_tariff.html', context)


def filter_car(request,city):
    vkl_name="Car's"
    location = city.lower()
    filter_vkl = vehicle.objects.filter(allot_city=location, category__name='CAR').all()
    operation_location= Location.objects.all()
    if not filter_vkl:
        raise Http404("No vehicles available in this city.")
    context = {
        'vkl_name':vkl_name,
        'city': city.capitalize(),
        'location': location,
        'filter_vkl': filter_vkl,
        'operation_location': operation_location,
    }
    return render(request, 'pages/filter_tariff_taxi.html', context)


def filter_taxi(request,city):
    vkl_name="Car's"
    location = city.lower()
    filter_vkl = vehicle.objects.filter(allot_city=location, category__name='CAR').all()
    operation_location= Location.objects.all()
    if not filter_vkl:
        raise Http404("No vehicles available in this city.")
    context = {
        'vkl_name':vkl_name,
        'city': city.capitalize(),
        'location': location,
        'filter_vkl': filter_vkl,
        'operation_location': operation_location,
    }
    return render(request, 'pages/filter_tariff_car.html', context)

def user_filter(request,city):
    location = city.lower()
    filter_vkl = vehicle.objects.filter(allot_city=location).all()
    operation_location= Location.objects.all()
    if request.method == 'POST':
        filter_st_date= request.POST.get('filter_from_date')
        filter_st_time= request.POST.get('filter_from_time')
        filter_end_date= request.POST.get('filter_to_date')
        filter_end_time= request.POST.get('filter_to_time')
        
    context = {
        'city': city.capitalize(),
        'location': location,
        'filter_vkl': filter_vkl,
        'filter_st_date': filter_st_date,
        'filter_st_time': filter_st_time,
        'filter_end_date': filter_end_date,
        'filter_end_time': filter_end_time,
        'operation_location': operation_location,
    }
    return render(request, 'pages/filter_vcl.html', context)



def user_filter_book(request,city,vkl_id):
    location = city.lower()
    filter_vkl = vehicle.objects.filter(allot_city=location, id=vkl_id).all()
    operation_location = Location.objects.all()
    user_detail = None
    if request.user.is_authenticated:
        user_detail = Users.objects.filter(phone_number=request.user.username).first()
    context = {
        'city': city.capitalize(),
        'location': location,
        'filter_vkl': filter_vkl,
        'operation_location': operation_location,
        'user_detail': user_detail,
    }
    if filter_vkl:
        vkl = filter_vkl[0]
        context.update({
            'hourly_rate_wo_driver': float(vkl.hourly_rate_wo_driver),
            'hourly_rate_with_driver': float(vkl.hourly_rate_with_driver),
            'daily_rate_wo_driver': float(vkl.daily_rate_wo_driver),
            'daily_rate_with_driver': float(vkl.daily_rate_with_driver),
            'weekly_rate_wo_driver': float(vkl.weekly_rate_wo_driver),
            'weekly_rate_with_driver': float(vkl.weekly_rate_with_driver),
            'fif_day_rate_wo_driver': float(vkl.fif_day_rate_wo_driver),
            'fif_day_rate_with_driver': float(vkl.fif_day_rate_with_driver),
            'monthly_rate_wo_driver': float(vkl.monthly_rate_wo_driver),
            'monthly_rate_with_driver': float(vkl.monthly_rate_with_driver),
        })
    return render(request, 'user/booking_popup.html', context)

def user_filter_facility(request,city):
    location = city.lower()
    filter_vkl = vehicle.objects.filter(allot_city=location).all()
    operation_location= Location.objects.all()
    if request.method == 'POST':
        filter_st_date= request.POST.get('filter_from_date')
        filter_st_time= request.POST.get('filter_from_time')
        filter_end_date= request.POST.get('filter_to_date')
        filter_end_time= request.POST.get('filter_to_time')
        
    context = {
        'city': city.capitalize(),
        'location': location,
        'filter_vkl': filter_vkl,
        'filter_st_date': filter_st_date,
        'filter_st_time': filter_st_time,
        'filter_end_date': filter_end_date,
        'filter_end_time': filter_end_time,
        'operation_location': operation_location,
    }
    
    return render(request, 'pages/filter_vcl.html', context)
    

def marketing_emails(request, city):
    if request.method == 'POST':
        Market_email = request.POST.get('marketing_emails')

        # Check if the email already exists
        dataem = Marketing_model.objects.filter(Marketing_email=Market_email).first()

        # If it exists, render the template
        if dataem is not None:
            return redirect('city_home', city=city)

        # If not, save it
        market_save = Marketing_model(Marketing_email=Market_email)
        market_save.save()
        send_mail(
             subject='Noreplay',
             message=f'Hello,\n\t Your Email is: {Market_email},\n\t Is subscribed for get latest information from SafeJourny',
             from_email='safejourney9090@gmail.com',  # Replace with your email
             recipient_list=[Market_email],
             fail_silently=False,
             
                )

    # Redirect after saving or if not POST
    return redirect('city_home', city=city)


def city_bike_rentals(request,city):
    
    return render(request, 'pages/index.html')




def user_login(request):

    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('user_phone')
        password = request.POST.get('user_password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # Fallback: filter User by phone number and password (not recommended for production, use authentication)
            try:
                user_obj = User.objects.get(username=username)
                if user_obj.check_password(password):
                    login(request, user_obj)
                    return redirect('city_home')
                else:
                    messages.error(request, 'Invalid mobile number or password.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid mobile number or password.')
    return render(request, 'user/user_login.html')

def user_signup(request):
    return redirect('send_otp')


def send_otp(request):
      # Ensure correct path

    if request.method == "POST":
        phone = request.POST.get("user_phone")
        user_captcha = request.POST.get("user_reg_captcha")
        session_captcha = request.session.get("captcha_text")

        if user_captcha is None or session_captcha is None:
            messages.error(request, "CAPTCHA session expired or missing.")
            return redirect('send_otp')

        if user_captcha.strip().upper() != session_captcha.upper():
            messages.error(request, "CAPTCHA verification failed.")
            return redirect('send_otp')

        # Continue with OTP logic
        otp = generate_otp()
        PhoneOTP.objects.update_or_create(phone=phone, defaults={"otp": otp, "is_verified": False})
        send_otp_via_whatsapp(phone, otp)
        messages.success(request, "OTP sent via WhatsApp.")
        return redirect('verify_otp')

    # For GET method, generate a new captcha
    captcha_img_path, captcha_text = generate_captcha()
    request.session["captcha_text"] = captcha_text

    return render(request, "user/user_register.html", {
        "captcha_img_path": captcha_img_path
    })


def reset_pass(request):
      # Ensure correct path

    if request.method == "POST":
        phone = request.POST.get("user_phone")
        email = request.POST.get("email")
        user_captcha = request.POST.get("user_reg_captcha")
        session_captcha = request.session.get("captcha_text")
        

        if user_captcha is None or session_captcha is None:
            messages.error(request, "CAPTCHA session expired or missing.")
            return redirect('reset_pass')

        if user_captcha.strip().upper() != session_captcha.upper():
            messages.error(request, "CAPTCHA verification failed.")
            return redirect('reset_pass')
        data=Users.objects.filter(user_id=phone, email=email).first()
        # Continue with OTP logic
        send_mail(
             subject='Reset Password',
             message=f'Hello,, Your username is: {data.user_id} and your password is: {data.password_hash}, Noreplay',
             from_email='safejourney9090@gmail.com',  # Replace with your email
             recipient_list=[email],
             fail_silently=False,
             
                )
        messages.success(request, "password sent through email")
        return redirect('user_login')

    # For GET method, generate a new captcha
    captcha_img_path, captcha_text = generate_captcha()
    request.session["captcha_text"] = captcha_text

    return render(request, "user/forget_pass.html", {
        "captcha_img_path": captcha_img_path
    })

'''   if request.method == "POST":
        phone = request.POST.get("user_phone")
        otp = generate_otp()
        PhoneOTP.objects.update_or_create(phone=phone, defaults={"otp": otp, "is_verified": False})
        #send_otp_via_whatsapp(phone, otp)
        messages.success(request, "OTP sent via WhatsApp.")
        return redirect('verify_otp')
    return render(request, "user/user_register.html")'''

def verify_otp(request):
    if request.method == "POST":
        username= request.POST.get("user_phone")
        user_full_name=request.POST.get("user_name")
        user_email= request.POST.get("user_email")
        phone = request.POST.get("user_phone")
        user_pass = request.POST.get("conferm_pass")
        otp = request.POST.get("user_otp")
        print(user_pass,username,user_full_name,user_email,phone,otp)
        try:
            phone_otp = PhoneOTP.objects.get(phone=phone, otp=otp, is_verified=False)
            phone_otp.is_verified = True
            phone_otp.save()
            if User.objects.filter(username=username).exists():
                messages.success(request,'Your email is already registered. Please login')
                return redirect('user_login')
            if User.objects.filter(email=user_email).exists():
                messages.success(request,'Your email is already registered. Please login')
                return redirect('user_login')
            messages.success(request, "OTP verified successfully.")
            
            user=User.objects.create_user(
                username=username,
                email=user_email,
                password=user_pass,
                first_name= user_full_name,
            )
            users=Users(
                email= user_email,
                user_id= username,
                first_name=user_full_name,
                password_hash=user_pass,
                phone_number=phone,
            )
            users.save()
            login_user=authenticate(username=username,password=user_pass)
            if login_user is not None:
                login(request, login_user)
            return redirect("user_login")
        except PhoneOTP.DoesNotExist:
            messages.error(request, "Invalid OTP. Please try again.")
    return render(request, "user/user_verify_otp.html")

@login_required(login_url='user_login')
def user_profile(request,city):
    location = city.lower()
    filter_vkl = vehicle.objects.filter(allot_city=location).all()
    operation_location= Location.objects.all()
    # After login or registration
    user = request.user
    request.session['user_id'] = user.id
    request.session['username'] = user.username
    request.session['email'] = user.email
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    email = request.session.get('email')
    user_detail = Users.objects.filter(phone_number=username).first()
    
    context = {
        'city': city.capitalize(),
        'location': location,
        'filter_vkl': filter_vkl,
        'user_detail':user_detail,
        'operation_location': operation_location,
    }


    return render(request, 'user/user_details.html',context)


def verify_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        user = authenticate(request, username=user_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'user/verify_user.html', {'error': 'Invalid credentials'})
    return render(request, 'user/verify_user.html')

@login_required(login_url='user_login')
def user_update_detail(request,city):
    location = city.lower()
    filter_vkl = vehicle.objects.filter(allot_city=location).all()
    operation_location= Location.objects.all()
    user_data= Users.objects.filter(phone_number=request.user.username).first()
    context = {
        'city': city.capitalize(),
        'location': location,
        'filter_vkl': filter_vkl,
        'operation_location': operation_location,
        'user_contact': contact_form_user.objects.filter(if_username=request.user.username).first(),
        'user': request.user,
        'user_data': user_data,
        
    }
    
    
    if request.method == 'POST':
        # Update only fields that are filled in the form
        user_data = Users.objects.filter(phone_number=request.user.username).first()
        if user_data:
            print(user_data.address)
        if user_data:
            # Try all possible field names for profile image
            user_profile_image = request.FILES.get('choose_file') or request.FILES.get('admin_addProduct_allform_input-file') or request.FILES.get('profile_img') or request.FILES.get('user_profile_img')
            print('Profile image received:', user_profile_image)
            if user_profile_image:
                user_data.user_profile_image = user_profile_image
            user_gender = request.POST.get('user_gender')
            if user_gender:
                user_data.user_gender = user_gender
            fname = request.POST.get('fname')
            if fname:
                user_data.first_name = fname
            lname = request.POST.get('lname')
            if lname:
                user_data.last_name = lname
            user_id = request.POST.get('user_id')
            if user_id:
                user_data.user_id = user_id
            drivers_license_number = request.POST.get('drivers_license_number')
            if drivers_license_number:
                user_data.driver_license_number = drivers_license_number
            addhar_number = request.POST.get('addhar_number')
            if addhar_number:
                user_data.addhar_number = addhar_number
            drivers_license_image = request.FILES.get('drivers_license_image') or request.FILES.get('admin_addProduct_allform_input-file_dl')
            if drivers_license_image:
                user_data.user_dl_image = drivers_license_image
            addhar_image = request.FILES.get('addhar_image') or request.FILES.get('admin_addProduct_allform_input-file_adhar')
            if addhar_image:
                user_data.user_addhar_image = addhar_image
            address_user = request.POST.get('address_user')
            if address_user:
                user_data.address = address_user
            user_data.save()
            return redirect('user_profile', city=city)
    return render(request, 'user/update_data.html', context)

def user_bookings(request, city):
    location = city.lower()
    filter_vkl = vehicle.objects.filter(allot_city=location).all()
    operation_location = Location.objects.all()
    user_name = request.user.username if request.user.is_authenticated else None
    user_detail = Users.objects.filter(phone_number=user_name).first() if user_name else None
    bookings = Booking.objects.filter(user__user_id=user_name) if user_name else Booking.objects.none()
    print('User Detail:', bookings)
    context = {
        'city': city.capitalize(),
        'location': location,
        'filter_vkl': filter_vkl,
        'operation_location': operation_location,
        'user_detail': user_detail,
        'bookings': bookings,
    }
    
    return render(request, 'user/user_bookings.html', context)




@login_required(login_url='user_login')
def confirm_booking(request, city):
    location = city.lower()
    filter_vkl = vehicle.objects.filter(allot_city=location).all()
    user_name = request.user.username if request.user.is_authenticated else None
    user_detail = Users.objects.filter(phone_number=user_name).first() if user_name else None
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            user_obj = Users.objects.filter(phone_number=user.username).first()
            #if not user_obj:
                #messages.error(request, "User details not found. Please update your profile before booking.")
                #return redirect('user_update_detail', city=city)
            user_name = user_obj.first_name if user_obj else 'Guest'
            user_email = user.email
            booking_number = request.POST.get('booking_number')
            print('Received booking number:', booking_number)
            vehicle_id = request.POST.get('Vehicle_id')
            start_date = request.POST.get('start_date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            end_date = request.POST.get('end_date')
            pickup_location_id = request.POST.get('pickup_location')
            dropoff_location_id = request.POST.get('dropoff_location')
            driver_choice = request.POST.get('Driverchoices')
            total_price = request.POST.get('totalPrice')
            
            vehicle_obj = vehicle.objects.filter(id=vehicle_id).first()
            print('Vehicle ID:', vehicle_id)
            print('Vehicle Object:', vehicle_obj)
            print(user_obj, vehicle_id, booking_number, start_time, start_date, end_date, end_time, pickup_location_id, dropoff_location_id, driver_choice, total_price)

            # Save booking to database
            Booking.objects.create(
                booking_number=booking_number,
                user=user_obj,
                vehicle=vehicle_obj,
                start_date=start_date,
                start_time=start_time,
                end_date=end_date,
                end_time=end_time,
                pickup_location_id=pickup_location_id,
                dropoff_location_id=dropoff_location_id,
                driver_choice=driver_choice,
                total_price=total_price,
                user_price=total_price
            )
            send_mail(
             subject='Booking Successful',
             message=f'Hello,{user_name}, Your Booking is confirmed.\n Booking Number: {booking_number}. \n Vehicle ID: {vehicle_id}.\n Start Date: {start_date},\n Start Time: {start_time},\n End Date: {end_date},\n End Time: {end_time},\n Pickup Location ID: {pickup_location_id},\n Dropoff Location ID: {dropoff_location_id},\n Driver Choice: {driver_choice},\n Total Price: {total_price}',
             
             from_email='safejourney9090@gmail.com',  # Replace with your email
             recipient_list=[user_email],
             fail_silently=False,
             
                )

            # Redirect or render a success page
            return redirect('city_home', city=city)
        else:
            return redirect('user_login')
    else:
        # Render booking form or error
        return render(request, 'user/booking_form.html', {'city': city})

def user_logout(request,city):
    logout(request)
    return redirect('index')  # Redirect to the index page after logout



