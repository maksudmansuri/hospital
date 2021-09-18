from django.db.models.base import Model
import patient
from django.contrib.auth.models import User
from hospital.models import HospitalServices, HospitalStaffDoctors, ServiceAndCharges
from accounts.models import CustomUser, Hospitals, Labs, Patients
from django.db import models

# Create your models here.

class Booking(models.Model):
    id                      =           models.AutoField(primary_key=True)
    patient                 =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hospitalstaffdoctor     =           models.ForeignKey(HospitalStaffDoctors, on_delete=models.CASCADE)
    amount                  =           models.FloatField()
    # hospital                =           models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    service                 =           models.ForeignKey(ServiceAndCharges, on_delete=models.CASCADE)
    booking_type            =           models.CharField(default="",blank=True,null=True,max_length=64)
    applied_date            =           models.CharField(default="",blank=True,null=True,max_length=64)
    applied_time            =           models.CharField(default="",blank=True,null=True,max_length=64)
    is_applied              =           models.BooleanField(default=True,blank=True,null=True)
    status                  =           models.CharField(default="",blank=True,null=True,max_length=64)
    accepted_date           =           models.DateTimeField(blank=True,null=True)
    taken_date              =           models.DateTimeField(blank=True,null=True)
    rejected_date           =           models.DateTimeField(blank=True,null=True)
    is_rejected             =           models.BooleanField(default=False)
    is_taken                =           models.BooleanField(default=False)
    is_accepted             =           models.BooleanField(default=False)
    is_cancelled            =           models.BooleanField(default=False)
    modified_time           =           models.TimeField(blank=True,null=True)
    modified_date           =           models.DateField(blank=True,null=True)
    add_note                =           models.CharField(max_length=5000,blank=True,null=True,default="")
    is_active               =           models.BooleanField(default=False)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()

class slot(models.Model):
    id                      =           models.AutoField(primary_key=True)
    patient                 =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lab                     =           models.ForeignKey(Labs, on_delete=models.CASCADE)
    applied_date            =           models.CharField(default="",blank=True,null=True,max_length=64)
    applied_time            =           models.CharField(default="",blank=True,null=True,max_length=64)
    is_applied              =           models.BooleanField(default=True,blank=True,null=True)
    status                  =           models.CharField(default="",blank=True,null=True,max_length=64)
    accepted_date           =           models.DateTimeField(blank=True,null=True)
    taken_date              =           models.DateTimeField(blank=True,null=True)
    rejected_date           =           models.DateTimeField(blank=True,null=True)
    is_rejected             =           models.BooleanField(default=False)
    is_taken                =           models.BooleanField(default=False)
    is_accepted             =           models.BooleanField(default=False)
    is_cancelled            =           models.BooleanField(default=False)
    modified_time           =           models.TimeField(blank=True,null=True)
    modified_date           =           models.DateField(blank=True,null=True)
    add_note                =           models.CharField(max_length=5000,blank=True,null=True,default="")
    is_active               =           models.BooleanField(default=False)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()


class TreatmentReliefPetient(models.Model):
    id                      =           models.AutoField(primary_key=True)
    booking                 =           models.ForeignKey(Booking, on_delete=models.CASCADE)
    patient                 =           models.ForeignKey(Patients, on_delete=models.CASCADE)
    amount_paid             =           models.FloatField()
    next_date               =           models.DateTimeField(blank=True,null=True)
    status                  =           models.CharField(default="",blank=True,null=True,max_length=64)
    is_active               =           models.BooleanField(default=False)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()

class PatientSymptons(models.Model):
    id                      =           models.AutoField(primary_key=True)
    TreatmentReliefPetient  =           models.ForeignKey(TreatmentReliefPetient,on_delete=models.CASCADE)
    symptom                 =           models.CharField(default="",blank=True,null=True,max_length=256)
    level                   =           models.CharField(default="",blank=True,null=True,max_length=256)
    is_active               =           models.BooleanField(default=False)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()

class PatientReports(models.Model):
    id                      =           models.AutoField(primary_key=True)
    TreatmentReliefPetient  =           models.ForeignKey(TreatmentReliefPetient,on_delete=models.CASCADE)
    Report                  =           models.CharField(default="",blank=True,null=True,max_length=256)
    Description             =           models.CharField(default="",blank=True,null=True,max_length=256)
    number_of_attempt       =           models.IntegerField(blank=True,null=True,default=1)
    is_active               =           models.BooleanField(default=False,blank=True,null=True)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()

class PatientMedicine(models.Model):
    id                      =           models.AutoField(primary_key=True)
    TreatmentReliefPetient  =           models.ForeignKey(TreatmentReliefPetient,on_delete=models.CASCADE)
    medicine_name           =           models.CharField(default="",blank=True,null=True,max_length=256)
    dose_per_day            =           models.CharField(default="",blank=True,null=True,max_length=256)
    number_of_days          =           models.IntegerField(blank=True,null=True,default=1)
    time_to_take            =           models.CharField(default="",blank=True,null=True,max_length=256)
    is_active               =           models.BooleanField(default=False,blank=True,null=True)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()

class PatientBottelAndInjections(models.Model):
    id                      =           models.AutoField(primary_key=True)
    TreatmentReliefPetient  =           models.ForeignKey(TreatmentReliefPetient,on_delete=models.CASCADE)
    type                    =           models.CharField(max_length=255,blank=True,null=True,default="")
    type_choice             =           ((1,"bottle"),(2,"Injection"))
    BI_content              =           models.FileField(choices=type_choice,blank=True,null=True,default="")
    desc                    =           models.CharField(max_length=255,blank=True,null=True,default="")
    is_active               =           models.BooleanField(default=False)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()


class LabTest(models.Model):
    id                      =           models.AutoField(primary_key=True)
    lab                     =           models.ForeignKey(Labs, on_delete=models.CASCADE)
    service                 =           models.ForeignKey(ServiceAndCharges, on_delete=models.CASCADE)
    slot                    =           models.ForeignKey(slot, on_delete=models.CASCADE)
    is_active               =           models.BooleanField(default=False)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()

class Orders(models.Model):
    id                      =           models.AutoField(primary_key=True)
    patient                 =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service                 =           models.ForeignKey(ServiceAndCharges, on_delete=models.CASCADE)
    amount                  =           models.FloatField()
    STATUS_TYPE_CHOICE      =           ((1,"Processed"),(2,"Successed"),(3,"Failed"),(4,"Cancelled"),(5,"Refunded"))
    status                  =           models.CharField(default="",blank=True,null=True,max_length=64,choices=STATUS_TYPE_CHOICE)    
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()