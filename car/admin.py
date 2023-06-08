from django.contrib import admin
from .models import Car, Privacy, Ads, Client
from django.contrib.auth.models import Group

# import-export plugin
# from import_export.admin import ImportExportModelAdmin


# @admin.action(description='Download data as a csv file')  
def download_csv(self, request, queryset):
    import csv
    f = open('some.csv', 'wb')
    writer = csv.writer(f)
    writer.writerow(["Name", "Phone Number"])
    for s in queryset:
        writer.writerow([s.name, s.phone_number ])

def download_csv_car_details(self, request, queryset):
    import csv
    f = open('some.csv', 'wb')
    writer = csv.writer(f)
    writer.writerow(["car_title", 
            "make_year", 
            "make_month",
            "car_manufacturer", 
            "car_model",
            "car_version",
            "car_color",
            "fuel_type",
            "transmission_type",
            "car_owner",
            "kilometer_driven",
            "expected_selling_price",
            "registration_type",
            "insurance_type",
            "registration_number",
            "car_description",
            "car_photo",
            "car_owner_phone_number",
            "car_city",
            "car_owner_name",
            "user"])
    for s in queryset:
        writer.writerow([s.car_title, 
            s.make_year, 
            s.make_month,
            s.car_manufacturer, 
            s.car_model,
            s.car_version,
            s.car_color,
            s.fuel_type,
            s.transmission_type,
            s.car_owner,
            s.kilometer_driven,
            s.expected_selling_price,
            s.registration_type,
            s.insurance_type,
            s.registration_number,
            s.car_description,
            s.car_photo,
            s.car_owner_phone_number,
            s.car_city,
            s.car_owner_name,
            s.user])

# class CarAdmin(ImportExportModelAdmin):
#     list_display =('car_title','car_manufacturer','car_model','car_version','car_owner','car_post_date','car_status','user')
#     list_filter =('car_manufacturer','car_status')
#     actions = ['download_csv_car_details']



# class ClientAdmin(admin.ModelAdmin):
#     list_display =('phone_number','name')
#     actions = ['download_csv']

# class ClientAdmin(ImportExportModelAdmin):
#     # resource_class = BookResource
#     list_display =('phone_number','name')
#     actions = ['download_csv']
    
# import-export plugin
# class ClientResource(resources.ModelResource):

#     pass



# Register your models here.
# admin.site.register(Car,CarAdmin)
admin.site.register(Car)
admin.site.register(Privacy)
admin.site.register(Ads)
# admin.site.register(Client,ClientAdmin)
admin.site.register(Client)

#change the header of admin dashboard
admin.site.site_header ='Admin Dashboard'