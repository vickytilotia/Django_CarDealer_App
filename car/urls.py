from django.contrib import admin
from django.urls import path, include
from car import views

urlpatterns = [
    
    path('', views.index, name = "index"),
    path('index.html', views.index, name = "index"),
    path('listing-classic.html', views.listing_classic, name = "listing-classic"),
    path('listing-detail.html/<int:myid>', views.listing_detail, name = "listing-detail"),
    path('listing-detail.html/<int:myid>/', views.listing_detail, name = "listing-detail"),
    path('post-vehicle.html', views.post_vehicle, name = "post-vehicle"),
    path('my-vehicles.html', views.my_vehicles, name = "my-vehicles"),
    path('profile-settings.html', views.profile_settings, name = "profile-settings"),
    path('about-us.html', views.about_us, name = "about-us"),
    path('search', views.search, name = "search"),
    path('sort.html', views.sort, name = "sort"),
    path('search_sort.html', views.sort, name = "sort"),
    # path('search_sort.html', views.search_sort, name = "search_sort"),
    path('privacy.html', views.privacy, name = "privacy"),
    
    path('signup', views.signup, name = "signup"),
    path('login', views.login_model, name = "login_model"),
    path('logout', views.logout_model, name = "logout_model"),
    path('delete_vehicles/<int:myid>/', views.delete_vehicles, name = "delete_vehicles"),

    # for otp verification
    path('submit_number', views.submit_number, name = "submit_number"),
    path('submit_otp', views.submit_otp, name = "submit_otp"),


    path('disclaimer', views.disclaimer, name = "disclaimer"),


]
