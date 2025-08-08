from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from safe_admin.models import ( Users, Location, vehicleCategory, 
                               vehicle, Booking, Payment, Review, 
                               Marketing_model,ServicesDetail,Staff)

def superuser_required(view_func=None, login_url=None):
    """
    Decorator for views that checks that the user is logged in and is a superuser.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

# Create your views here.

def admin_logout(request):
    logout(request)
    return render(request, 'admin/admin_login.html')


def collect_user_data():
    all_user = Users.objects.all()
    all_location = Location.objects.all()
    all_vehicleCategory = vehicleCategory.objects.all()
    all_vehicle = vehicle.objects.all()
    all_booking = Booking.objects.all()
    all_payment = Payment.objects.all()
    all_review = Review.objects.all()
    all_marketing = Marketing_model.objects.all()
    all_services = ServicesDetail.objects.all()
    all_staff = Staff.objects.all()

    return {
        'all_user': all_user,
        'all_location': all_location,
        'all_vehicleCategory': all_vehicleCategory,
        'all_vehicle': all_vehicle,
        'all_booking': all_booking,
        'all_payment': all_payment,
        'all_review': all_review,
        'all_marketing': all_marketing,
        'all_services': all_services,
        'all_staff': all_staff,
    }
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user= authenticate( username=username, password=password)
        if not request.user.is_authenticated or not request.user.is_superuser:
            return render(request, 'admin/admin_login.html', {'error': 'You must be logged in as an admin to access this page.'})
        elif user and user.is_superuser:
            login(request, user)
            # User is authenticated
            #return redirect('admin_panel')  # Redirect to the admin panel
            return render(request, 'admin/admin_panel.html')
        else:
            # Authentication failed
            return render(request, 'admin/admin_login.html', {'error': 'Invalid credentials'})
    return render(request, 'admin/admin_login.html')




#@login_required(login_url='admin_login')
def admin_panel(request):
    context = collect_user_data()
    totaluser = context['all_user'].count()
    print(totaluser)
    print('All cities in Location:')
    for loc in context['all_location']:
        print(loc.city)
    return render(request, 'admin/admin_panel.html', context)


@superuser_required(login_url='admin_login')
def manage_staff(request, staff_id):
    context = collect_user_data()
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        staff.username = request.POST.get('name')
        staff.email = request.POST.get('email')
        staff.phone_number = request.POST.get('phone_number')
        staff.image= request.FILES.get('image', staff.image)  # Keep existing image if not updated
        staff.save()
        context['message'] = 'Staff member updated successfully.'
        context['staff'] = staff  # Include the updated staff object in the context

        return redirect('admin_panel', context)  # Redirect to the admin panel after saving
    return render(request, 'admin/edit_staff.html', {'staff': staff})

@superuser_required(login_url='admin_login')
def admin_payment_list(request):
    context = collect_user_data()
    return render(request, 'admin/payment_list.html', context)



