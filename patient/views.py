from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from accounts.models import HospitalPhones, Hospitals, Patients
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.contrib import messages
from django.urls.base import reverse
from django.core.files.storage import FileSystemStorage



# Create your views here.
class patientdDashboardViews(SuccessMessageMixin,ListView):
    def get(self, request, *args, **kwargs):
        try: 
            patient = get_object_or_404(Patients, admin=request.user.id)

            if patient.fisrt_name and patient.last_name and patient.address and patient.city and patient.zip_Code and patient.state and patient.country and patient.dob and patient.profile_pic and patient.gender and patient.bloodgroup:
                return render(request,"patient/index.html")            
            
            messages.add_message(request,messages.ERROR,"Some detail still Missing !")
            
            return render(request,"patient/patient_update.html",{'patient':patient})
        except Exception as e:
            return HttpResponse(e)
    

class patientdUpdateViews(SuccessMessageMixin,UpdateView):
    def get(self, request, *args, **kwargs):
        try: 
            patient = get_object_or_404(Patients, admin=request.user.id)
            return render(request,"patient/patient_update.html",{'patient':patient})
        except Exception as e:
            return HttpResponse(e)
    
    def post(self,request, *agrs, **kwargs):
        profile_pic = request.FILES.get('profile_pic')
        name_title = request.POST.get('name_title')
        alternate_mobile = request.POST.get('alternate_mobile')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_Code = request.POST.get('zip_Code')
        print(zip_Code)
        state = request.POST.get('state')
        print(state)
        country = request.POST.get('country')
        print(country)
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        bloodgroup = request.POST.get('bloodgroup')
        try:            
            user= request.user
            user.patients.name_title=name_title
            user.patients.fisrt_name=user.first_name
            user.patients.last_name=user.last_name
            if profile_pic:
                fs=FileSystemStorage()
                filename1=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename1)
                user.patients.profile_pic=profile_pic_url
                user.profile_pic = profile_pic_url
            user.patients.alternate_mobile=alternate_mobile
            user.patients.address=address
            user.patients.city=city
            user.patients.state=state
            user.patients.zip_Code=zip_Code
            user.patients.country=country
            user.patients.gender=gender
            user.patients.dob=dob
            user.patients.bloodgroup=bloodgroup
            user.patients.save()            
            user.save()
            messages.add_message(request,messages.SUCCESS,"User Detail updates Successfully !")
            return HttpResponseRedirect(reverse("patient_home"))
        except Exception as e:
            HttpResponse(e)

class HospitalListViews(ListView):
    def get(self, request, *args, **kwargs):
        hospitals = Hospitals.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True)
        param = {'hospitals':hospitals}  
        return render(request,"patient/hospital_details.html",param)
    
class HospitalDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id']
        hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
        hospitalcontact = HospitalPhones.objects.filter(hospital=hospital).first()
        param = {'hospital':hospital,'hospitalcontact':hospitalcontact}  
        return render(request,"patient/hospital_details.html",param)