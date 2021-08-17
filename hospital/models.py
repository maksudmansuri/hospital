from django.db import models
from accounts.models import HospitalDoctors, Hospitals,CustomUser

# Create your models here.

class HospitalStaffs(models.Model):
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
        return self.first_name + " " + self.last_name

class Departments(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="")
    hospital_staff      =models.ForeignKey(HospitalStaffs, on_delete=models.CASCADE)
    department_head     =models.CharField(max_length=256,blank=True,null=True,default="")
    department_name     =models.CharField(max_length=256,blank=True,null=True,default="")
    mobile              =models.CharField(max_length=256,blank=True,null=True,default="")
    email               =models.CharField(max_length=256,blank=True,null=True,default="")
    is_active           =models.BooleanField(default=False)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects             =models.Manager()

    def __str__(self):
        return self.department_head


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
