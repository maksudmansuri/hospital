from django.urls.base import reverse
from hospital import urls
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from accounts import views
from django.shortcuts import render
from django.views.generic import View,CreateView,DetailView,DeleteView,ListView,UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from hospital.models import ContactPerson, HospitalMedias, HospitalStaffs, Insurances
from accounts.models import CustomUser, HospitalPhones, Hospitals
from django.urls import reverse

# Create your views here. 

# class indexView(SuccessMessageMixin,ListView):
#     pass
    # model = CustomUser
    # template_name = "hospital/hospital_update.html"
    # def get(self, request, *args, **kwargs): 
    #    return render(request,"hospital/hospital_update.html")

class hospitaldDashboardViews(SuccessMessageMixin,ListView):
    model = Hospitals
    template_name = "hospital/index.html"


class hospitalUpdateViews(SuccessMessageMixin,UpdateView):
    UserModel=get_user_model()
    def get(self, request, *args, **kwargs):
        hospital = None
        # contacts = None
        # insurances = None
        try:
            hospital = Hospitals.objects.get(admin=request.user.id)
            contacts = HospitalPhones.objects.filter(hospital=hospital)
            insurances = Insurances.objects.filter(hospital=hospital)
        except hospital.DoesNotExist:
            return None
        param={'hospital':hospital,'insurances':insurances,'contacts':contacts}
        return render(request,"hospital/hospital_update.html",param) 
    
    def post(self, request, *args, **kwargs):
        hopital_name = request.POST.get("hopital_name")
        specialist = request.POST.get("specialist")
        about = request.POST.get("about")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        address = address1 + address2
        city = request.POST.get("city")
        pin_code = request.POST.get("pin_code")
        state = "Gujarat"
        country = "India"
        landline = request.POST.get("landline")
        establishment_year = request.POST.get("establishment_year")
        registration_number = request.POST.get("registration_number")
        registration_proof = request.POST.get("registration_proof")
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        linkedin = request.POST.get("linkedin")
        twitter = request.POST.get("twitter")
        website = request.POST.get("website")
        # add media
        media_type_list = request.POST.getlist("media_type[]")
        media_content_list = request.POST.getlist("media_content[]")
        #contact detail
        hospital_mobile_list= request.POST.getlist("hospital_mobile[]")
        hospital_email_list = request.POST.getlist("hospital_email[]")
        #insuarance
        insurance_type_list = request.POST.getlist("insurance_type[]")
        insurance_name_list = request.POST.getlist("insurance_name[]")
        #hidden Ids from for loop
        insurances_id = request.POST.getlist("insurances_id[]")
        contacts_id = request.POST.getlist("contacts_id[]")
        # user creation Data
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        # mobile = request.POST.get("phone")
        alternate_mobile = request.POST.get("alternate_mobile")
        # email = request.POST.get("email")
        name_title = request.POST.get("name_title")

        print("we are indside a add hspitals")

        UserModel=get_user_model()
        try:
            UserModel = CustomUser.objects.get(id=request.user.id)
        except UserModel.DoesNotExist:
            return None        
        #creeating new hospital
        #hospital = Hospitals(admin=UserModel,hopital_name=hopital_name,about=about,registration_number=registration_number,address=address,city=city,pin_code=pin_code,state=state,country=country,landline=area_landine,specialist=specialist,registration_proof=registration_proof,establishment_year=establishment_year,alternate_mobile=alternate_mobile,website=website,linkedin=linkedin,facebook=facebook,instagram=instagram,twitter=twitter)
        hospital = Hospitals.objects.get(admin=UserModel)
        hospital.hopital_name=hopital_name
        hospital.about=about
        hospital.registration_number=registration_number
        hospital.address1=address1
        hospital.address2=address2
        hospital.city=city
        hospital.pin_code=pin_code
        hospital.state=state
        hospital.country=country
        hospital.landline=landline
        hospital.specialist=specialist
        hospital.registration_proof=registration_proof
        hospital.establishment_year=establishment_year
        hospital.alternate_mobile=alternate_mobile
        hospital.website=website
        hospital.linkedin=linkedin
        hospital.facebook=facebook
        hospital.instagram=instagram
        hospital.twitter=twitter
        hospital.is_appiled=True
        hospital.is_verified=False
        hospital.save()
        #edit customUSer
        hospital.admin.first_name=first_name
        hospital.admin.last_name=last_name
        hospital.admin.name_title=name_title       
        hospital.admin.save()
        print("Hospital and user saved")     
        i=0
        for media_content in media_content_list:
            fs=FileSystemStorage()
            filename=fs.save(media_content.name,media_content)
            media_url=fs.url(filename)
            # print(media_content[1],"gjkbdgjdfg")
            if media_type_list[0]:                    
                hospital.profile_pic=media_url
                print("inside zero in images")                    
                hospital.save()
            hospital_media = HospitalMedias(hospital=hospital,media_type=media_type_list[i],media_content=media_url)
            hospital_media.is_active=True
            hospital_media.is_default=True
            hospital_media.save() 
            i=i+1  
        print("Meida saved")          
        j=0
        hos_mobiles = HospitalPhones.objects.filter(is_active=True) 
        for hospital_mobile in hospital_mobile_list:
            contact_id = contacts_id[j]
            if contact_id == "blank" and hospital_mobile != "" and hospital_email_list[j] != "" :                
                if hos_mobiles:
                    for hos_mobile in hos_mobiles:
                        if hospital_mobile == hos_mobile.hospital_mobile or hospital_email_list[j] == hos_mobile.hospital_email :
                            messages.add_message(self.request,messages.ERROR," Mobile number or email id is already exist")
                        else: 
                            hospitalphone =HospitalPhones(hospital=hospital,hospital_mobile=hospital_mobile,hospital_email=hospital_email_list[j])
                            hospitalphone.is_active =True
                            hospitalphone.save()
                else: 
                    hospitalphone =HospitalPhones(hospital=hospital,hospital_mobile=hospital_mobile,hospital_email=hospital_email_list[j])
                    hospitalphone.is_active =True
                    hospitalphone.save()
            else:
                if hospital_mobile != "" or hospital_email_list[j] != "" :
                    hospitalphone = HospitalPhones.objects.get(id=contact_id)
                    hospitalphone.hospital_mobile = hospital_mobile
                    hospitalphone.hospital_email = hospital_email_list[j]
                    hospitalphone.save()
            j=j+1

        print("phone saved")
        k=0
        for insurance_name in insurance_name_list:
            insurance_id = insurances_id[k]
            if insurance_id == "blank" and insurance_name != "" : 
                insurance =Insurances(hospital=hospital,insurance_type=insurance_type_list[k],insurance_name=insurance_name)
                insurance.is_active =True
                insurance.save()
            else:
                if insurance_name != "":
                    insurance = Insurances.objects.get(id=insurance_id)
                    insurance.insurance_type = insurance_type_list[k]
                    insurance.insurance_name = insurance_name
                    insurance.save()

            k=k+1
        print("insurance saved")      
        
        print("All data saved")

        messages.add_message(self.request,messages.SUCCESS,"Hospital Account Created Succesfully")
        return HttpResponseRedirect(reverse("hospital_dashboard"))
        # except:
        #     return render(request,"radmin/hospital_add.html")  

class manageStaffView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            staffs = HospitalStaffs.objects.filter(hospital=hospital)
        except hospital.DoesNotExist:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_staff"))        
        param={'hospital':hospital,'staffs':staffs}
        return render(request,"hospital/manage_staff.html",param)

    def post(self, request, *args, **kwargs):
        name_title = request.POST.get("name_title")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        mobile = request.POST.get("phone")
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        hospital=Hospitals.objects.get(admin=request.user)
        hospitalstaff = HospitalStaffs(hospital=hospital,name_title=name_title,first_name=first_name,last_name=last_name,email=email,mobile=mobile,is_active=active)
        hospitalstaff.save()
        # except:
        #     messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
        #     return HttpResponseRedirect(reverse("manage_staff"))
        return HttpResponseRedirect(reverse("manage_staff"))

def updateStaff(request):
     if request.method == "POST":
        id= request.POST.get("id")
        name_title = request.POST.get("name_title")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        mobile = request.POST.get("phone")
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        hospitalstaff = HospitalStaffs.objects.get(id=id)
        print(hospitalstaff)
        hospitalstaff.name_title=name_title
        hospitalstaff.first_name=first_name
        hospitalstaff.last_name=last_name
        hospitalstaff.email=email
        hospitalstaff.is_active=active
        hospitalstaff.save()
        print(hospitalstaff)
        messages.add_message(request,messages.SUCCESS,"Successfully Updated")
        return HttpResponseRedirect(reverse("manage_staff"))

def activeStaff(request,id):
    staff = HospitalStaffs.objects.get(id=id)
    if staff:
        staff.is_active=True        
        staff.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_staff"))

def deactiveStaff(request,id):
    staff = HospitalStaffs.objects.get(id=id)
    if staff:
        staff.is_active=False        
        staff.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_staff"))

def deleteHospitalStaff(request,id):
    staff = HospitalStaffs.objects.get(id=id)
    staff.delete()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("manage_staff"))

class manageDepartmentclassView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            staffs = HospitalStaffs.objects.filter(hospital=hospital)
        except hospital.DoesNotExist:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_staff"))        
        param={'hospital':hospital,'staffs':staffs}
        return render(request,"hospital/manage_staff.html",param)

    def post(self, request, *args, **kwargs):
        name_title = request.POST.get("name_title")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        mobile = request.POST.get("phone")
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        hospital=Hospitals.objects.get(admin=request.user)
        hospitalstaff = HospitalStaffs(hospital=hospital,name_title=name_title,first_name=first_name,last_name=last_name,email=email,mobile=mobile,is_active=active)
        hospitalstaff.save()
        # except:
        #     messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
        #     return HttpResponseRedirect(reverse("manage_staff"))
        return HttpResponseRedirect(reverse("manage_staff"))
