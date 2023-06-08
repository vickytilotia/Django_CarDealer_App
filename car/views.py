from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Car, Client, Privacy, Ads
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.core.management import call_command

# installed rate limit
from django_ratelimit.decorators import ratelimit

import random

# Create your views here.
def index(request):
    
    allcars = Car.objects.all().filter(vehicle_type = "Car")
    total_vehicles = allcars.count()
    context = {'allcars':allcars, 'total_vehicles':total_vehicles}
    return render(request, 'index-3.html', context)

# list all cars on used car page
def listing_classic(request):
    
    allcars = Car.objects.all()

    paginator = Paginator(allcars, 8) # Show 8 contacts per page.

    page_number = request.GET.get('page')
    allcars= paginator.get_page(page_number)
    total_vehicles = Car.objects.count()
    context = {'allcars':allcars, 'total_vehicles':total_vehicles}
    return render(request, 'listing-classic.html', context)

# display car details
def listing_detail(request, myid):
    
    car = Car.objects.filter(id=myid)

    # using django sessions
    # is otp verified or not?
    otp_verified = False
    if request.session.get('otp_verified') != None:
        otp_verified = True
        print(otp_verified)
    else:
        otp_verified = False
    
    context = {'car':car[0], 'otp_verified':otp_verified}

    return render(request, 'listing-detail.html', context)

# search page function
def search(request):
    if request.method=='GET':
        car_city = request.GET.get('city')
        vehicle_type = request.GET.get('vehicle_type')
        slider_range = request.GET.get('slider')
        range_list = slider_range.split(",")
        min = range_list[0]
        max = range_list[1]
        print(min,max)
        price_result = Car.objects.filter(expected_selling_price__range=(min, max))
        # price_result = Car.objects.raw('select expected_selling_price from car_car where expected_selling_price between "'+min+'" and "'+max+'" ')
        
        allcars = Car.objects.all()
        # vehicle_type=vehicle_type
        if car_city == "Select Location" and vehicle_type == "Select Vehicle Type" :
            result = Car.objects.all()
        elif car_city == "Select Location" :
            result = Car.objects.all().filter(vehicle_type= vehicle_type)
        elif vehicle_type == "Select Vehicle Type":
            result = Car.objects.all().filter(car_city = car_city)
        else:
            result = Car.objects.all().filter(car_city = car_city, vehicle_type= vehicle_type)
        
        # intersecting two dictionaries

        final_dict = result & price_result
        print(price_result)
        print(result)
        print("this is ")
        print(final_dict)

        

        # total_vehicles = len(final_dict)
        total_vehicles = 6
      

        context = {'result':final_dict, 'allcars':allcars, 'total_vehicles':total_vehicles}


        return render(request, 'search.html', context)


def sort(request):
    if request.method=='GET':
        sort = request.GET.get('sort')
        print(sort)
        sorted = Car.objects.all()
        if sort == "Price (low to high)" :
            sorted = Car.objects.order_by("expected_selling_price")
            # sorted = Car.objects.order_by("expected_selling_price")

            # set a variable so that sort.html change its choice according to the previous choice 
            low_to_high = True

        elif sort == "Price (high to low)" :
            sorted = Car.objects.order_by("-expected_selling_price")

            # set a variable so that sort.html change its choice according to the previous choice 
            low_to_high = False

        total_vehicles = sorted.count()
        allcars = Car.objects.all()
        context = {'sorted':sorted,'allcars':allcars, 'total_vehicles':total_vehicles, 'low_to_high': low_to_high}

        return render(request, 'sort.html', context)


def search_sort(request):
    if request.method=='GET':
        sort = request.GET.get('sort')
        print(sort)
        

        # use session to get allcars from search page 
        all_search_page_cars = request.session.get('allcars')
        print(all_search_page_cars)

        if sort == "Price (low to high)" :
            sorted = Car.objects.order_by("expected_selling_price")
            # sorted = Car.objects.order_by("expected_selling_price")
        elif sort == "Price (high to low)" :
            sorted = Car.objects.order_by("-expected_selling_price")



        total_vehicles = sorted.count()
        allcars = Car.objects.all()
        context = {'sorted':sorted,'allcars':allcars, 'total_vehicles':total_vehicles}

        return render(request, 'sort.html', context)


@login_required(login_url='/#loginModal')
def post_vehicle(request):
    # return HttpResponse("this is homepage")

    if request.method=='POST':
        car_title = request.POST['car_title']
        make_year = request.POST['make_year']
        make_month = request.POST['make_month']
        car_manufacturer = request.POST['car_manufacturer']
        car_model = request.POST['car_model']
        car_version = request.POST['car_version']
        car_color = request.POST['car_color']
        fuel_type = request.POST['fuel_type']
        transmission_type = request.POST['transmission_type']
        car_owner = request.POST['car_owner']
        kilometer_driven = request.POST['kilometer_driven']
        expected_selling_price = request.POST['expected_selling_price']
        registration_type = request.POST['registration_type']
        insurance_type = request.POST['insurance_type']
        registration_number = request.POST['registration_number']
        car_description = request.POST['car_description']
        car_photo = request.FILES['car_photo']
        car_owner_phone_number = request.POST['car_owner_phone_number']
        car_city = request.POST['car_city']
        car_owner_name = request.POST['car_owner_name']
        user = request.user

        if kilometer_driven.isnumeric()==False:
            kilometer_driven = None
        if make_year.isnumeric()==False:
            make_year = None
        if expected_selling_price.isnumeric()==False:
            expected_selling_price = None
        if car_owner_phone_number.isnumeric()==False:
            car_owner_phone_number = None

        
        car = Car(
            car_title=car_title, 
            make_year=make_year, 
            make_month=make_month,
            car_manufacturer=car_manufacturer, 
            car_model=car_model,
            car_version=car_version,
            car_color=car_color,
            fuel_type=fuel_type,
            transmission_type=transmission_type,
            car_owner=car_owner,
            kilometer_driven=kilometer_driven,
            expected_selling_price=expected_selling_price,
            registration_type=registration_type,
            insurance_type=insurance_type,
            registration_number=registration_number,
            car_description=car_description,
            car_photo=car_photo,
            car_owner_phone_number=car_owner_phone_number,
            car_city=car_city,
            car_owner_name=car_owner_name,
            user=user,

        )
        

        car.save()


    return render(request, 'post-vehicle.html', {})

@login_required(login_url='/#loginModal')
def my_vehicles(request):
    cars = Car.objects.filter(user = request.user)
    context = {'cars':cars}
    
    
    return render(request, 'my-vehicles.html', context)

@login_required(login_url='/#loginModal')
def delete_vehicles(request, myid):
    obj = get_object_or_404(Car, id=myid)
    try:
        call_command('dbbackup')
    except:
        pass
    if request.method == "POST":
        obj.delete()
        return redirect('/my-vehicles.html')
    
    
    return render(request, 'my-vehicles.html', {})

@login_required(login_url='/#loginModal')
def profile_settings(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            # return redirect('/')
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, 'Please retry for password change')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile-settings.html', {
        'form': form
    })
    # return render(request, 'profile-settings.html', {})


# @ratelimit(key='ip', rate='3/m', block=True)
def about_us(request):
    # return HttpResponse("this is homepage")
    return render(request, 'about-us.html', {})




@ratelimit(key='ip', rate='10/h', block=True)
def signup(request):
    if request.method == 'POST':
        #get the form parameters
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        

        #checks
        if len(username)>15:
            messages.error(request, "Username must be under 15 characters")
            # return redirect('/')
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            print(request.META['HTTP_REFERER'])
            # return redirect(request.META['HTTP_REFERER'])
            return redirect(signup_url)
        
        # unique username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            # return redirect('/')
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            print(request.META['HTTP_REFERER'])
            # return redirect(request.META['HTTP_REFERER'])
            return redirect(signup_url)
        
        # unique email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            # return redirect('/')
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            print(request.META['HTTP_REFERER'])
            # return redirect(request.META['HTTP_REFERER'])
            return redirect(signup_url)
        
        if pass1 != pass2:
            messages.error(request, "Password do Not match")
            # return redirect('/')
            # return redirect(request.META['HTTP_REFERER'])
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            return redirect(signup_url)
        
        if len(pass1)<6:
            messages.error(request, "Password length must be greater than 6")
            # return redirect('/')
            # return redirect(request.META['HTTP_REFERER'])
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            return redirect(signup_url)




        # create the user
        myuser = User.objects.create_user(username,email,pass1)
        myuser.save()
        messages.success(request, "Your account has been created")
        
        
        # login with same details
        user = authenticate(username=username, password =pass1)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            # return redirect('/')
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, "Invalid Credentials")
            # return redirect('/')
            # return redirect(request.META['HTTP_REFERER'])
            login_url = request.META['HTTP_REFERER'] + "#loginModal"
            return redirect(login_url)

        # return redirect('/')
        return redirect(request.META['HTTP_REFERER'])
    
    else:
        return HttpResponse('404- Not Found')


@ratelimit(key='ip', rate='10/h', block=True)  
def login_model(request):
    if request.method == 'POST':
        #get the form parameters
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        
        user = authenticate(username=loginusername, password =loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            # return redirect('/')
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, "Invalid Credentials")
            # return redirect('/')
            # return redirect(request.META['HTTP_REFERER'])
            login_url = request.META['HTTP_REFERER'] + "#loginModal"
            return redirect(login_url)
    return HttpResponse("404- Not Found")

def logout_model(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    # return redirect('/')
    return redirect(request.META['HTTP_REFERER'])


def privacy(request):
    # return HttpResponse("this is homepage")
    
    policy = Privacy.objects.all()
    context = {'policy':policy[0]}
    
    
    return render(request, 'privacy.html', context)


@ratelimit(key='ip', rate='10/h', block=True)
def submit_number(request):
    global message
    global ph_number
    global otp_car_id
    if request.method == 'POST':
        #get the form parameters
        ph_number = request.POST['phone_number']
        ph_number = int(ph_number)
        request.session['session_phone_number'] = ph_number
        ph_name = request.POST['phone_name']
        request.session['session_phone_name'] = ph_name
        
        otp_car_id = request.POST['car_id']
        request.session['session_otp_car_id'] = otp_car_id
        print(request.session['session_phone_number'])
        # session for phone number which is already in database
        if  Client.objects.filter(phone_number=int(request.session['session_phone_number'])).exists():
            request.session['otp_verified'] = True
            print('You are : ', request.session.get('session_phone_number'))
            # rel_url = 'listing-detail.html/'+str(request.session['session_otp_car_id'])+'/#get_details'
            rel_url = 'listing-detail.html/'+str(request.session['session_otp_car_id'])

            return redirect(rel_url)
        else:
            
            request.session['session_otp']=generate_otp_message(request)
            print(request.session['session_otp'])
            
            # return HttpResponseRedirect(request.path_info)
            re_url = 'listing-detail.html/'+str(request.session['session_otp_car_id'])+'/#submit_otp'
            # return render(request, re_url, context)
            return redirect(re_url)

    else:
        return HttpResponse("404- Not Found for sumit number")

def submit_otp(request):
    if request.method == 'POST':
        #get the form parameters
        get_otp = request.POST['get_otp']
        print(get_otp)
        if int(get_otp) == int(request.session['session_otp']):
            
            client = Client(name=request.session['session_phone_name'], phone_number=int(request.session['session_phone_number']))
            client.save()
            print("These are your details")

            # sessions for otp verified person
            request.session['otp_verified'] = True

            # rel_url = 'listing-detail.html/'+str(request.session['session_otp_car_id'])+'/#get_details'
            rel_url = 'listing-detail.html/'+str(request.session['session_otp_car_id'])

            return redirect(rel_url)

        else:
            r_url = 'listing-detail.html/'+str(request.session['session_otp_car_id'])+'/#submit_otp'
            return redirect(r_url)
        
    return HttpResponse("404- Not Found for submit otp")




def disclaimer(request):
    # return HttpResponse("this is homepage")
    
    return render(request, 'Disclaimer.html')
