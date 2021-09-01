import hospital
from django.db import models
from django.db.models.fields import AutoField, CharField, IntegerField, related
from accounts.models import DoctorForHospital, HospitalDoctors, Hospitals,CustomUser

# Create your models here.

class HospitalStaffs(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="")
    name_title          =models.CharField(max_length=256,blank=True,null=True,default="")
    first_name          =models.CharField(max_length=256,blank=True,null=True,default="")
    last_name           =models.CharField(max_length=256,blank=True,null=True,default="")
    mobile              =models.CharField(max_length=256,blank=True,null=True,default="")
    email               =models.CharField(max_length=256,blank=True,null=True,default="")
    ssn_id              =models.IntegerField(default=1)
    is_active           =models.BooleanField(default=False)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()
    
    def __str__(self):
        return self.name_title + self.first_name + " " + self.last_name

class HospitalStaffDoctors(models.Model):
    id                  =models.AutoField(primary_key=True)
    email               =models.EmailField(default="", max_length=254)
    doctor              =models.ForeignKey(HospitalDoctors, on_delete=models.CASCADE)
    hospital            =models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    ssn_id              =models.CharField(max_length=50,default="",blank=True,null=True)
    joindate            =models.DateField(blank=True,null=True,default="")
    is_virtual_available=models.BooleanField(blank=True,null=True,default=False)   
    is_online           =models.BooleanField(blank=True,null=True,default=False)   
    is_active           =models.BooleanField(blank=True,null=True,default=False) 
    created_at          =models.DateTimeField(auto_now=True)
    updated_at          =models.DateTimeField(auto_now=True)
    objects             =models.Manager()
    
    def __str__(self):
        return self.doctor.fisrt_name + " " + self.doctor.last_name

class HospitalStaffDoctorSchedual(models.Model):
    id                           =models.AutoField(primary_key=True)
    hospital                     =models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    hospitalstaffdoctor          =models.ForeignKey(HospitalStaffDoctors, on_delete=models.CASCADE)
    SHIFT_CHOICE                 =(("Morning","Morning"),("Noon","Noon"),("Evening","Evening"),("All-Day","All-Day"))
    DAY_CHOICE                 =(("YES","YES"),("NO","NO"))
    shift                        =models.CharField(choices=SHIFT_CHOICE, max_length=50,default="",blank=True,null=True)
    monday                       =models.CharField(max_length=500,default="",blank=True,null=True) 
    tuesday                       =models.CharField(max_length=500,default="",blank=True,null=True) 
    wednesday                    =models.CharField(max_length=500,default="",blank=True,null=True) 
    thursday                     =models.CharField(max_length=500,default="",blank=True,null=True) 
    friday                       =models.CharField(max_length=500,default="",blank=True,null=True) 
    saturday                     =models.CharField(max_length=500,default="",blank=True,null=True) 
    sunday                       =models.CharField(max_length=500,default="",blank=True,null=True) 
    work                         =models.CharField(max_length=500,default="",blank=True,null=True)               
    start_time                   =models.TimeField(auto_now=False,blank=True,null=True)
    end_time                     =models.TimeField(auto_now=False,blank=True,null=True)
    is_active                    =models.BooleanField(blank=True,null=True,default=True)
    created_at                   =models.DateTimeField(auto_now=True)
    updated_at                   =models.DateTimeField(auto_now=True)
    objects                      =models.Manager()

class Departments(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="")
    hospital_staff_doctor=models.ForeignKey(HospitalStaffDoctors, on_delete=models.CASCADE)
    department_head     =models.CharField(max_length=256,blank=True,null=True,default="")
    department_name     =models.CharField(max_length=256,blank=True,null=True,default="")
    mobile              =models.CharField(max_length=256,blank=True,null=True,default="")
    email               =models.CharField(max_length=256,blank=True,null=True,default="")
    is_active           =models.BooleanField(default=False)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects             =models.Manager()

    def __str__(self):
        return self.department_name

class RoomOrBadTypeandRates(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="")
    ROOM_TYPE_CHOICE    =((1,"A.C"),(2,"Non-A.C"),(3,"General"))
    room_type           =models.CharField(choices=ROOM_TYPE_CHOICE, max_length=50,default="",blank=True,null=True)
    rooms_price         =models.IntegerField(default=0)
    is_active           =models.BooleanField(default=False)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects             =models.Manager()
    
    def __str__(self):
        return self.room_type

class HospitalRooms(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="")
    department          =models.ForeignKey(Departments,on_delete=models.CASCADE,default="")
    room                =models.ForeignKey(RoomOrBadTypeandRates,on_delete=models.CASCADE,default="")
    floor               =models.CharField(max_length=50,default="",blank=True,null=True)
    room_no             =models.CharField(max_length=50,blank=True,null=True,default=1)    
    occupied            =models.BooleanField(default=False,blank=True,null=True)    
    is_active           =models.BooleanField(default=False,blank=True,null=True)
    created_at          =models.DateTimeField(auto_now=True)
    updated_at          =models.DateTimeField(auto_now=True)
    objects             =models.Manager()
    
    def __str__(self):
        return self.room_no

class ContactPerson(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="")
    name_title          =models.CharField(max_length=256,blank=True,null=True,default="")
    first_name          =models.CharField(max_length=256,blank=True,null=True,default="")
    last_name           =models.CharField(max_length=256,blank=True,null=True,default="")
    mobile              =models.CharField(max_length=256,blank=True,null=True,default="")
    email               =models.CharField(max_length=256,blank=True,null=True,default="")
    is_active           =models.BooleanField(default=False)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()
    
    def __str__(self):
        return self.hospital.hopital_name +" Department of" + self.department

class Insurances(models.Model):
    id                      =           models.AutoField(primary_key=True)
    hospital                =           models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    insurance_type          =           models.CharField(max_length=255,blank=True,null=True,default="")
    insurance_type_choice   =           ((1,"CashLess"),(2,"No Cahsless"))
    insurance_name          =           models.CharField(choices=insurance_type_choice,blank=True,null=True,default="",max_length=255)
    is_active               =           models.BooleanField(default=False)         
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    def __str__(self):
        return self.hospital.hopital_name

class DepartmentPhones(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="")
    department          =models.ForeignKey(Departments,on_delete=models.CASCADE,default="")
    mobile              =models.CharField(max_length=256,blank=True,null=True,default="")
    email               =models.CharField(max_length=256,blank=True,null=True,default="")
    is_active           =models.BooleanField(default=False)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()
    
    def __str__(self):
        return self.hospital.hopital_name +" Department of" + self.department

class HospitalMedias(models.Model):
    id                      =           models.AutoField(primary_key=True)
    hospital                =           models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    media_type              =           models.CharField(max_length=255,blank=True,null=True,default="")
    media_type_choice       =           ((1,"Image"),(2,"Video"))
    media_content           =           models.FileField(choices=media_type_choice,blank=True,null=True,default="")
    is_active               =           models.BooleanField(default=False)     
    is_default              =           models.BooleanField(default=False)     
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    def __str__(self):
        return self.hospital.hopital_name

class HospitalTreatments(models.Model):
    id                      =           models.AutoField(primary_key=True)
    hospital                =           models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    department              =           models.OneToOneField(Departments, on_delete=models.CASCADE)
    doctor                  =           models.ForeignKey(HospitalDoctors, on_delete=models.CASCADE)
    treatment_name          =           models.CharField(max_length=255,blank=True,null=True,default="")
    treatment_rate          =           models.CharField(max_length=255,blank=True,null=True,default="")
    is_active               =           models.BooleanField(default=False)     
    is_default              =           models.BooleanField(default=False)     
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    def __str__(self):
        return self.hospital.hopital_name

# class shiftsDaysTime(models.Model):
#     id = models.AutoField(primary_key=True)
#     number_of_Days = models.IntegerField()
#     shift_start_time = models.TimeField(auto_now=False, auto_now_add=False)
#     shift_end_time = models.TimeField(auto_now=False, auto_now_add=False)
