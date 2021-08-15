from django.core.files.storage import FileSystemStorage
from hospital.models import ContactPerson, HospitalMedias, Insurances
from accounts.models import CustomUser, HospitalPhones, Hospitals
from django.shortcuts import render
from django.views.generic import View,CreateView,DetailView,DeleteView,ListView,UpdateView
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.
   
def indexView(request): 
    return render(request,"radmin/index.html")

def hospitalallView(request): 
    return render(request,"radmin/hospital_all.html")

class hospitalAddViews(SuccessMessageMixin,CreateView):
    success_message = "Hosppital Added Successfuly"
    error_massage = "Try again Error occured"  
    def get(self, request, *args, **kwargs): 
       return render(request,"radmin/hospital_add.html") 
    
    def post(self, request, *args, **kwargs):
        hopital_name = request.POST.get("hopital_name")
        specialist = request.POST.get("specialist")
        about = request.POST.get("about")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        address = address1 + address2
        city = request.POST.get("city")
        pin_code = request.POST.get("pin_code")
        state = request.POST.get("state")
        country = request.POST.get("country")
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
        # user creation Data
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        mobile = request.POST.get("phone")
        alternate_mobile = request.POST.get("alternate_mobile")
        email = request.POST.get("email")
        name_title = request.POST.get("name_title")

        print("we are indside a add hspitals")
      
        hospital = Hospitals(admin=1,hopital_name=hopital_name,about=about,registration_number=registration_number,address=address,city=city,pin_code=pin_code,state=state,country=country,landline=landline,specialist=specialist,registration_proof=registration_proof,establishment_year=establishment_year,establishment_number=registration_number,alternate_mobile=alternate_mobile,website=website,linkedin=linkedin,facebook=facebook,instagram=instagram,twitter=twitter)
        hospital.is_appiled=True
        hospital.is_verified=False
        hospital.save()
        print("Hospital saved")     
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
        for hospital_mobile in hospital_mobile_list:
            hospitalphone =HospitalPhones(hospital=hospital,hospital_mobile=hospital_mobile,hospital_email=hospital_email_list[j])
            hospitalphone.is_active =True
            hospitalphone.save()              
            j=j+1
        print("phone saved")
        k=0
        for insurance_name in insurance_name_list:
            insurance =Insurances(hospital=hospital,insurance_type=insurance_type_list[k],insurance_name=insurance_name)
            insurance.is_active
            insurance.save()
            k=k+1
        print("insurance saved")

        contactperson = ContactPerson(email=email,first_name=first_name,last_name=last_name,mobile=mobile,hospital=hospital,name_title=name_title)
        contactperson.is_active()
        contactperson.save()
        print("All data saved")

        
        return render(request,"radmin/hospital_add.html")
        # except:
        #     return render(request,"radmin/hospital_add.html")  

def hospitalUpdateView(request): 
    return render(request,"radmin/doctor_add.html")

def hospitalDeleteView(request): 
    return render(request,"radmin/doctor_add.html")


def virtualView(request): 
    return render(request,"radmin/virtual.html")

def doctorallView(request): 
    return render(request,"radmin/doctor_all.html")

def doctor_addView(request): 
    return render(request,"radmin/doctor_add.html")

def appoinmentView(request): 
    return render(request,"radmin/appoinment.html")

def doctorprofileView(request): 
    return render(request,"radmin/doctor_profile.html")

def doctorscheduleView(request): 
    return render(request,"radmin/doctor_schedule.html")
    
def patientlistView(request): 
    return render(request,"radmin/patient_list.html")

def patientaddtView(request): 
    return render(request,"radmin/patient_add.html")
    
def patientprofileView(request): 
    return render(request,"radmin/patient_profile.html")
    
def patientinvoiceView(request): 
    return render(request,"radmin/patient_invoice.html")

def accidentsView(request): 
    return render(request,"radmin/accidents.html")

def labsviews(request): 
    return render(request,"radmin/labs.html")

def departmentviews(request): 
    return render(request,"radmin/department.html")
 
def invicesviews(request): 
    return render(request,"radmin/invoices.html") 
 
def paymentsviews(request): 
    return render(request,"radmin/payments.html")
 
def expencesviews(request): 
    return render(request,"radmin/expences.html")

 