from django.contrib import admin
from accounts.models import CustomUser,HospitalDoctors, HospitalPhones, AdminHOD, DoctorForHospital ,Hospitals
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, AuthorAdmin)
admin.site.register(HospitalDoctors)
admin.site.register(AdminHOD)
admin.site.register(HospitalPhones)
admin.site.register(DoctorForHospital)
admin.site.register(Hospitals)