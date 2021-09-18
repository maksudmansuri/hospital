from django.core.files.storage import FileSystemStorage
import pharmacy
from django.http.response import HttpResponse, HttpResponseRedirect
from accounts.models import Pharmacy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.urls import reverse
from django.contrib import messages
# Create your views here.


class LabDashboardViews(SuccessMessageMixin,ListView):
    def get(self, request, *args, **kwargs):
      
            # hospital = Hospitals.objects.get(admin=request.user.id)
            # contacts = HospitalPhones.objects.filter(hospital=hospital)
            # insurances = Insurances.objects.filter(hospital=hospital)

            # if hospital.hopital_name and hospital.about and hospital.address1 and hospital.city and hospital.pin_code and hospital.state and hospital.country and hospital.landline and hospital.registration_proof and hospital.profile_pic and hospital.establishment_year and hospital.registration_number and hospital.alternate_mobile and contacts:
                return render(request,"pharmacy/index.html")
            
            
            # messages.add_message(request,messages.ERROR,"Some detail still Missing !")
            # param={'hospital':hospital,'insurances':insurances,'contacts':contacts}
            # return render(request,"hospital/hospital_update.html",param)
       
    # def get(self,request):
    #     print("hello in m  in lab")
    #     return render(request,"lab/index.html")

class PharmacyUpdateViews(SuccessMessageMixin,UpdateView):
    def get(self, request, *args, **kwargs):
        # hospital = None
        # # contacts = None
        # # insurances = None
        try:
            pharmacy = Pharmacy.objects.get(admin=request.user.id)
            # contacts = HospitalPhones.objects.filter(hospital=hospital)
            # insurances = Insurances.objects.filter(hospital=hospital)
        except Exception as e:
            return HttpResponse(e)
        param={'pharmacy':pharmacy}
        return render(request,"pharmacy/pharmacy_update.html",param) 
    
    def post(self, request, *args, **kwargs):
        pharmacy_name = request.POST.get("pharmacy_name")
        specialist = request.POST.get("specialist")
        profile_pic = request.FILES.get("profile_pic")

        about = request.POST.get("about")
        address = request.POST.get("address")
        city = request.POST.get("city")
        pin_code = request.POST.get("pin_code")
        state = "Gujarat"
        country = "India"
        landline = request.POST.get("landline")
        establishment_year = request.POST.get("establishment_year")
        registration_number = request.POST.get("registration_number")
        registration_proof = request.FILES.get("registration_proof")
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        linkedin = request.POST.get("linkedin")
        twitter = request.POST.get("twitter")
        website = request.POST.get("website")
        # user creation Data
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        # mobile = request.POST.get("phone")
        alternate_mobile = request.POST.get("alternate_mobile")
        # email = request.POST.get("email")
        name_title = request.POST.get("name_title")

        print("we are indside a add hspitals")
        try:
            pharmacy = Pharmacy.objects.get(admin=request.user.id)
            pharmacy.pharmacy_name=pharmacy_name
            pharmacy.about=about
            pharmacy.registration_number=registration_number
            pharmacy.address=address
            pharmacy.city=city
            pharmacy.pin_code=pin_code
            pharmacy.state=state
            pharmacy.country=country
            pharmacy.landline=landline

            if profile_pic:
                fs=FileSystemStorage()
                filename1=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename1)
                pharmacy.profile_pic=profile_pic_url

            print(registration_proof)
            if registration_proof:
                fs=FileSystemStorage()
                filename=fs.save(registration_proof.name,registration_proof)
                registration_proof_url=fs.url(filename)
                pharmacy.registration_proof=registration_proof_url
            pharmacy.establishment_year=establishment_year
            pharmacy.alternate_mobile=alternate_mobile
            pharmacy.website=website
            pharmacy.linkedin=linkedin
            pharmacy.facebook=facebook
            pharmacy.instagram=instagram
            pharmacy.twitter=twitter
            pharmacy.is_appiled=True
            pharmacy.is_verified=False
            pharmacy.save()
            #edit customUSer
            pharmacy.admin.first_name=first_name
            pharmacy.admin.last_name=last_name
            pharmacy.admin.name_title=name_title       
            pharmacy.admin.save()           
                    
            
            print("All data saved")

            messages.add_message(request,messages.SUCCESS,"Succesfully Updated")
            
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            
        return HttpResponseRedirect(reverse("pharmacy_update"))
    
class ViewAppointmentViews(SuccessMessageMixin,View):
    pass

def deleteServicesViews(request):
    pass