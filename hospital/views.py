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
from hospital.models import ContactPerson, DepartmentPhones, Departments, HospitalMedias, HospitalRooms, HospitalStaffDoctorSchedual, HospitalStaffDoctors, HospitalStaffs, Insurances, RoomOrBadTypeandRates
from accounts.models import CustomUser, DoctorForHospital, HospitalDoctors, HospitalPhones, Hospitals
from django.urls import reverse

# Create your views here. 

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
        mobile = request.POST.get("mobile")
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
            doctors = HospitalStaffDoctors.objects.filter(hospital=hospital)
            departments = Departments.objects.filter(hospital=hospital)
        except hospital.DoesNotExist:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_staff"))        
        param={'hospital':hospital,'staffs':staffs,'departments':departments,'doctors':doctors}
        return render(request,"hospital/manage_deparment.html",param)

    def post(self, request, *args, **kwargs):
        department_name = request.POST.get("department_name")
        hospital_staff_doctor1 = request.POST.get("hospital_staff_doctor")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        hospital=Hospitals.objects.get(admin=request.user)
        hospital_staff_doctor = HospitalStaffDoctors.objects.get(id=hospital_staff_doctor1)
        hospitaldepartments = Departments(hospital=hospital,department_name=department_name,hospital_staff_doctor=hospital_staff_doctor,email=email,mobile=mobile,is_active=active)
        hospitaldepartments.save()
        # except:
        #     messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
        #     return HttpResponseRedirect(reverse("manage_staff"))
        return HttpResponseRedirect(reverse("manage_department"))

def updateDepartment(request):
     if request.method == "POST":
        id= request.POST.get("id")
        department_name = request.POST.get("department_name")
        hospital_staff = request.POST.get("hospital_staff")
        email = request.POST.get("email")
        mobile = request.POST.get("phone")
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        hospitalstaff1 = HospitalStaffs.objects.get(id=hospital_staff)
        hospitaldepartment = Departments.objects.get(id=id)
        hospitaldepartment.department_name=department_name
        hospitaldepartment.hospital_staff=hospitalstaff1
        hospitaldepartment.email=email
        hospitaldepartment.is_active=active
        hospitaldepartment.save()
        messages.add_message(request,messages.SUCCESS,"Successfully Updated")
        return HttpResponseRedirect(reverse("manage_department"))

def activeDepartment(request,id):
    hospitaldepartment = Departments.objects.get(id=id)
    if hospitaldepartment:
        hospitaldepartment.is_active=True        
        hospitaldepartment.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_department"))

def deactiveDepartment(request,id):
    hospitaldepartment = Departments.objects.get(id=id)
    if hospitaldepartment:
        hospitaldepartment.is_active=False        
        hospitaldepartment.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_department"))

def deleteHospitalDepartment(request,id):
    hospitaldepartment = Departments.objects.get(id=id)
    hospitaldepartment.delete()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("manage_department"))

class manageRoomclassView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            roooOrbadtypeandrates = RoomOrBadTypeandRates.objects.filter(hospital=hospital)
            rooms = HospitalRooms.objects.filter(hospital=hospital)
            prices = RoomOrBadTypeandRates.objects.filter(hospital=hospital)
            departments = Departments.objects.filter(hospital=hospital)
            # departments = Departments.objects.filter(hospital=hospital)
        except hospital.DoesNotExist:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_staff"))        
        param={'hospital':hospital,'rooms':rooms,'departments':departments,'prices':prices}
        return render(request,"hospital/manage_room.html",param)

    def post(self, request, *args, **kwargs):
        floor = request.POST.get("floor")
        room_no = request.POST.get("room_no")
        room = request.POST.get("room")
        department = request.POST.get("department")
        print(room)
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        hospital=Hospitals.objects.get(admin=request.user)
        department = Departments.objects.get(id=department)
        room_type = RoomOrBadTypeandRates.objects.get(id=room)
        hospitalroom = HospitalRooms(hospital=hospital,department=department,room=room_type,floor=floor,room_no=room_no,is_active=active)
        hospitalroom.save()
        # except:
        #     messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
        #     return HttpResponseRedirect(reverse("manage_staff"))
        return HttpResponseRedirect(reverse("manage_room"))

def updateRoom(request):
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
        hospitalroom = HospitalRooms.objects.get(id=id)
        hospitalroom.name_title=name_title
        hospitalroom.first_name=first_name
        hospitalroom.last_name=last_name
        hospitalroom.email=email
        hospitalroom.is_active=active
        hospitalroom.save()
        messages.add_message(request,messages.SUCCESS,"Successfully Updated")
        return HttpResponseRedirect(reverse("manage_room"))

def activeRoom(request,id):
    hospitalroom = HospitalRooms.objects.get(id=id)
    if hospitalroom:
        hospitalroom.is_active=True        
        hospitalroom.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_room"))

def deactiveRoom(request,id):
    hospitalroom = HospitalRooms.objects.get(id=id)
    if hospitalroom:
        hospitalroom.is_active=False        
        hospitalroom.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_room"))

def deleteHospitalRoom(request,id):
    hospitalroom = HospitalRooms.objects.get(id=id)
    hospitalroom.delete()
    messages.add_message(request,messages.SUCCESS,"Successfully Deleted")
    return HttpResponseRedirect(reverse("manage_room"))

def PriceCreate(request):
    if request.method == "POST":
        rooms_price = request.POST.get("rooms_price") 
        room_type = request.POST.get("room_type")
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            roomorbadtypeandrate= RoomOrBadTypeandRates(hospital=hospital,room_type=room_type,rooms_price=rooms_price,is_active=active)
            roomorbadtypeandrate.save()
        except hospital.DoesNotExist:
            messages.add_message(request,messages.ERROR,"user not available")
        return HttpResponseRedirect(reverse("manage_room"))

def deletePrice(request,id):
    roomorbadtypeandrate = RoomOrBadTypeandRates.objects.get(id=id)
    roomorbadtypeandrate.delete()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("manage_room"))

class manageDoctorView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            doctors = HospitalStaffDoctors.objects.filter(hospital=hospital)
        except hospital.DoesNotExist:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_staff"))        
        param={'hospital':hospital,'doctors':doctors}
        return render(request,"hospital/manage_doctor.html",param)        

    def post(self, request, *args, **kwargs):
        #for CustomUSer creation
        first_name = request.POST.get("fisrt_name")
        last_name = request.POST.get("last_name")
        name_title = request.POST.get("name_title")
        username = first_name + last_name
        user_type = 3
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        profile_pic = request.FILES.get("profile_pic")
        # for HospitalDoctor user Creation
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        ssn_id = request.POST.get("ssn_id")
        country = request.POST.get("country")
        zip_Code = request.POST.get("zip_Code")
        degree = request.POST.get("degree")
        specialist = request.POST.get("specialist")
        dob = request.POST.get("dob")
        alternate_mobile = request.POST.get("alternate_mobile")
        gender = request.POST.get("gender")
        # for Hospital staff user creation
        joindate = request.POST.get("joindate")
        is_active = request.POST.get("is_active")
        is_virtual = request.POST.get("is_virtual_available")
        print(is_virtual)
        is_virtual_available = False
        if is_virtual == "Yes":
            is_virtual_available = True
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        linkedin = request.POST.get("linkedin")
        active = False
        if is_active == "on":
            active= True
        
        print(profile_pic)
        profile_pic_url = ""
        if profile_pic:
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            media_url=fs.url(filename)
            profile_pic_url = media_url
        print(profile_pic_url)
        hospital=Hospitals.objects.get(admin=request.user)

        doctor = HospitalDoctors(fisrt_name=first_name,last_name=last_name,address=address,city=city,state=state,country=country,zip_Code=zip_Code,phone=phone,degree=degree,dob=dob,alternate_mobile=alternate_mobile,profile_pic=profile_pic_url,gender=gender,facebook=facebook,instagram=instagram,linkedin=linkedin,specialist=specialist)        
        doctor.save()
       
        staffdoctor= HospitalStaffDoctors(doctor=doctor,hospital=hospital,joindate=joindate,is_active=active,ssn_id=ssn_id,is_virtual_available=is_virtual_available,email=email)
        staffdoctor.save()
       
        # except:
        #     messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
        #     return HttpResponseRedirect(reverse("manage_staff"))
        return HttpResponseRedirect(reverse("manage_doctor"))

def updateDoctor(request):
     if request.method == "POST":
        id= request.POST.get("id")
        doctorid= request.POST.get("doctorid")
        #for CustomUSer creation
        first_name = request.POST.get("fisrt_name")
        last_name = request.POST.get("last_name")
        name_title = request.POST.get("name_title")
        username = first_name + last_name
        user_type = 3
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        profile_pic = request.FILES.get("profile_pic")
        # for HospitalDoctor user Creation
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        ssn_id = request.POST.get("ssn_id")
        country = request.POST.get("country")
        zip_Code = request.POST.get("zip_Code")
        dob = request.POST.get("dob")
        alternate_mobile = request.POST.get("alternate_mobile")
        gender = request.POST.get("gender")
        # for Hospital staff user creation
        joindate = request.POST.get("joindate")
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        is_virtual = request.POST.get("is_virtual_available")
        print("hello virtual")
        print(is_virtual)
        is_virtual_available = False
        if is_virtual == "Yes":
            is_virtual_available = True
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        linkedin = request.POST.get("linkedin")
        
        

        hospital=Hospitals.objects.get(admin=request.user)
        doctor=HospitalDoctors.objects.get(id=doctorid)

        staffdoctor= HospitalStaffDoctors(id=id)
        staffdoctor.hospital=hospital
        staffdoctor.joindate=joindate
        staffdoctor.is_active=active
        staffdoctor.ssn_id=ssn_id
        staffdoctor.email=email
        staffdoctor.doctor=doctor
        staffdoctor.is_virtual_available=is_virtual_available
        staffdoctor.save()
        staffdoctor.doctor.fisrt_name=first_name
        staffdoctor.doctor.last_name=last_name
        staffdoctor.doctor.address=address
        staffdoctor.doctor.city=city
        staffdoctor.doctor.state=state
        staffdoctor.doctor.country=country
        staffdoctor.doctor.zip_Code=zip_Code
        staffdoctor.doctor.phone=phone        
        staffdoctor.doctor.facebook=facebook
        staffdoctor.doctor.instagram=instagram
        staffdoctor.doctor.linkedin=linkedin
        staffdoctor.doctor.dob=dob
        staffdoctor.doctor.alternate_mobile=alternate_mobile
        profile_pic_url = staffdoctor.doctor.profile_pic
        if profile_pic:
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            media_url=fs.url(filename)
            profile_pic_url = media_url
        staffdoctor.doctor.profile_pic=profile_pic_url
        staffdoctor.doctor.gender=gender
        staffdoctor.doctor.save()
        return HttpResponseRedirect(reverse("manage_doctor"))

def activeDoctor(request,id):
    doctor = HospitalStaffDoctors.objects.get(id=id)
    if doctor:
        doctor.is_active=True        
        doctor.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_doctor"))

def deactiveDoctor(request,id):
    doctor = HospitalStaffDoctors.objects.get(id=id)
    if doctor:
        doctor.is_active=False        
        doctor.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_doctor"))

def deleteHospitalDoctor(request,id):
    doctor = HospitalStaffDoctors.objects.get(id=id)
    doctor.delete()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("manage_doctor"))


class manageDoctorSchedualView(SuccessMessageMixin,View):
    def get(self, request, *args, **kwargs):
        id=kwargs["id"]
        print(id)
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            doctors = HospitalStaffDoctors.objects.filter(hospital=hospital)
            hospitalstaffdoctor = HospitalStaffDoctors.objects.get(id=id)
            print(hospitalstaffdoctor)
            hospitalstaffdoctorschedual = HospitalStaffDoctorSchedual.objects.filter(hospitalstaffdoctor=hospitalstaffdoctor)
        except hospital.DoesNotExist:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_staff"))        
        param={'hospital':hospital,'doctors':doctors,'hospitalstaffdoctor':hospitalstaffdoctor,'hospitalstaffdoctorschedual':hospitalstaffdoctorschedual}
        return render(request,"hospital/doctor_schedule.html",param)        

    def post(self, request, *args, **kwargs):
        #for CustomUSer creation
        id=kwargs["id"]
        days = request.POST.get("days")
        work = request.POST.get("work")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        hospitalstaffdoctor = HospitalStaffDoctors.objects.get(id=id)
        hospital=Hospitals.objects.get(admin=request.user)
        hospitalstaffdoctorschedual= HospitalStaffDoctorSchedual(hospital=hospital,hospitalstaffdoctor=hospitalstaffdoctor,end_time=end_time,work=work,days=days,start_time=start_time)
        hospitalstaffdoctorschedual.save()
       
        # except:
        #     messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
        #     return HttpResponseRedirect(reverse("manage_staff"))
        return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':id}))

def updateDoctorSchedual(request ,id):
     if request.method == "POST":
        id= request.POST.get("id")
        doctorid= request.POST.get("doctorid")
        #for CustomUSer creation
        first_name = request.POST.get("fisrt_name")
        last_name = request.POST.get("last_name")
        name_title = request.POST.get("name_title")
        username = first_name + last_name
        user_type = 3
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        profile_pic = request.FILES.get("profile_pic")
        # for HospitalDoctor user Creation
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        ssn_id = request.POST.get("ssn_id")
        country = request.POST.get("country")
        zip_Code = request.POST.get("zip_Code")
        dob = request.POST.get("dob")
        alternate_mobile = request.POST.get("alternate_mobile")
        gender = request.POST.get("gender")
        # for Hospital staff user creation
        joindate = request.POST.get("joindate")
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        is_virtual = request.POST.get("is_virtual_available")
        print("hello virtual")
        print(is_virtual)
        is_virtual_available = False
        if is_virtual == "Yes":
            is_virtual_available = True
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        linkedin = request.POST.get("linkedin")
        
        

        hospital=Hospitals.objects.get(admin=request.user)
        doctor=HospitalDoctors.objects.get(id=doctorid)

        staffdoctor= HospitalStaffDoctors(id=id)
        staffdoctor.hospital=hospital
        staffdoctor.joindate=joindate
        staffdoctor.is_active=active
        staffdoctor.ssn_id=ssn_id
        staffdoctor.email=email
        staffdoctor.doctor=doctor
        staffdoctor.is_virtual_available=is_virtual_available
        staffdoctor.save()
        staffdoctor.doctor.fisrt_name=first_name
        staffdoctor.doctor.last_name=last_name
        staffdoctor.doctor.address=address
        staffdoctor.doctor.city=city
        staffdoctor.doctor.state=state
        staffdoctor.doctor.country=country
        staffdoctor.doctor.zip_Code=zip_Code
        staffdoctor.doctor.phone=phone        
        staffdoctor.doctor.facebook=facebook
        staffdoctor.doctor.instagram=instagram
        staffdoctor.doctor.linkedin=linkedin
        staffdoctor.doctor.dob=dob
        staffdoctor.doctor.alternate_mobile=alternate_mobile
        profile_pic_url = staffdoctor.doctor.profile_pic
        if profile_pic:
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            media_url=fs.url(filename)
            profile_pic_url = media_url
        staffdoctor.doctor.profile_pic=profile_pic_url
        staffdoctor.doctor.gender=gender
        staffdoctor.doctor.save()
        return HttpResponseRedirect(reverse("manage_doctor"))

def deleteHospitalDoctorschedual(request,id):
    doctor = HospitalStaffDoctors.objects.get(id=id)
    doctor.delete()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("manage_doctor"))
