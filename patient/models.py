import datetime
import json
import channels
from channels.layers import get_channel_layer
from django.contrib import admin
from django.db.models.fields import IntegerField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import request
import pharmacy
from django.db.models.base import Model
import patient
from django.contrib.auth.models import User
from hospital.models import HospitalRooms, HospitalServices, HospitalStaffDoctors, ServiceAndCharges
from accounts.models import CustomUser, Hospitals, Labs, Patients, Pharmacy
from django.db import models
from asgiref.sync import async_to_sync,sync_to_async


# Create your models here.
class ForSome(models.Model):
    id                  =models.AutoField(primary_key=True)
    name_title          =models.CharField(max_length=50,blank=True,null=True,default="")
    patient             =models.ForeignKey(Patients,on_delete=models.CASCADE)
    fisrt_name          =models.CharField(max_length=250,blank=True,null=True,default="")
    email               =models.EmailField(max_length=254,blank=True,null=True,default="xyz@gmail.com")
    last_name           =models.CharField(max_length=250,blank=True,null=True,default="")
    address             =models.CharField(max_length=500,blank=True,null=True,default="")
    city                =models.CharField(max_length=250,blank=True,null=True,default="")
    state               =models.CharField(max_length=250,blank=True,null=True,default="")
    country             =models.CharField(max_length=250,blank=True,null=True,default="")
    zip_Code            =models.CharField(max_length=250,blank=True,null=True,default="")
    age                 =models.IntegerField(blank=True,null=True)
    phone               =models.CharField(max_length=250,blank=True,null=True,default="")
    ID_proof            =models.FileField(upload_to="someone/ID/images/%Y/%m/%d/",blank=True,null=True,default="")
    gender              =models.CharField(max_length=255,null=True,default="")
    add_notes           =models.CharField(max_length=5000,null=True,default="")
    bloodgroup          =models.CharField(max_length=255,null=True,default="")
    is_appiled          =models.BooleanField(blank=True,null=True,default=False)
    is_verified         =models.BooleanField(blank=True,null=True,default=False)
    is_active           =models.BooleanField(blank=True,null=True,default=False)
    created_at          =models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at          =models.DateTimeField(auto_now_add=True,null=True,blank=True)
    objects             =models.Manager()
    
    def __str__(self): 
        return self.fisrt_name +" "+ self.last_name
 
class Booking(models.Model):
    id                      =           models.AutoField(primary_key=True)
    patient                 =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    for_whom                =           models.ForeignKey(ForSome, on_delete=models.CASCADE,null=True,blank=True)
    hospitalstaffdoctor     =           models.ForeignKey(HospitalStaffDoctors, on_delete=models.CASCADE,null=True,blank=True)
    amount                  =           models.FloatField()
    hospital                =           models.ForeignKey(Hospitals, on_delete=models.CASCADE,null=True,blank=True)
    service                 =           models.ForeignKey(ServiceAndCharges, on_delete=models.CASCADE,null=True,blank=True)
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
    booking_type            =           models.CharField(default="OPD",blank=True,null=True,max_length=64)
    is_active               =           models.BooleanField(default=False)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ['-created_at']

    @staticmethod
    def give_booking_details(id):
        instance = Booking.objects.filter(id=id).first()        
        data = {}
        data['booking_id'] = instance.id
        data['amount'] = instance.amount
        data['status'] = instance.status
        progress_pecentage = 0
        if instance.status == "":
            progress_pecentage = 20
        if instance.status == "accepted":
            progress_pecentage = 50
        if instance.status == "taken":
            progress_pecentage = 100
        if instance.status == "rejected":
            progress_pecentage = 100

        data['progress'] = progress_pecentage
        return data

    # def gettime(request):
    #     instance = Booking.objects.filter(patient=request.user).first()
    #     lefttime = datetime.datetime.now() - instance.created_at)
    #     return lefttime


@receiver(post_save, sender=Booking)
def booking_status_handler(sender,instance,created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {}
        data['booking_id'] = instance.id
        data['amount'] = instance.amount
        data['status'] = instance.status

        progress_pecentage = 0
        if instance.status == "":
            progress_pecentage = 20
        if instance.status == "accepted":
            progress_pecentage = 50
        if instance.status == "taken":
            progress_pecentage = 100
        if instance.status == "rejected":
            progress_pecentage = 100

        data['progress'] = progress_pecentage

        async_to_sync(channel_layer.group_send)(
            'booking_%s' % instance.id,{
                'type' : 'booking_status',
                'value' : json.dumps(data)
            }
        )

class ReBooking(models.Model):
    id                      =           models.AutoField(primary_key=True)
    booking                 =           models.ForeignKey(Booking, on_delete=models.CASCADE)    
    amount                  =           models.FloatField()
    service                 =           models.ForeignKey(ServiceAndCharges, on_delete=models.CASCADE)
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

    class Meta:
        ordering = ['-created_at']

class Admited(models.Model):
    id                      =           models.AutoField(primary_key=True)
    booking                 =           models.ForeignKey(Booking, on_delete=models.CASCADE,null=True,blank =True)
    booking                 =           models.ForeignKey(ReBooking, on_delete=models.CASCADE,null=True,blank =True)
    bed_charges             =           models.FloatField(null=True,blank =True,default=0)
    other_charges           =           models.FloatField(null=True,blank =True,default=0)
    doctor_charges          =           models.FloatField(null=True,blank =True,default=0)
    tax_charges             =           models.FloatField(null=True,blank =True,default=0)
    total_charges           =           models.FloatField(null=True,blank =True,default=0)
    hospital                =           models.ForeignKey(Hospitals, on_delete=models.CASCADE,null=True,blank =True)
    room                    =           models.ForeignKey(HospitalRooms, on_delete=models.CASCADE,null=True,blank =True)
    status                  =           models.CharField(default="",blank=True,null=True,max_length=64)
    admined_date            =           models.DateTimeField(blank=True,null=True)
    discharge_date          =           models.DateTimeField(blank=True,null=True)
    is_rejected             =           models.BooleanField(default=False)
    is_cancelled            =           models.BooleanField(default=False)
    add_note                =           models.CharField(max_length=5000,blank=True,null=True,default="")
    is_active               =           models.BooleanField(default=False)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ['-created_at']

class FollowedUp(models.Model):
    id                      =           models.AutoField(primary_key=True)
    booking                 =           models.ForeignKey(Booking, on_delete=models.CASCADE)
    next_date               =           models.DateTimeField(auto_now_add=True)
    previous_date           =           models.DateTimeField(auto_now_add=True)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ['next_date']

class Slot(models.Model):
    id                      =           models.AutoField(primary_key=True)
    patient                 =           models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    for_whom                =           models.ForeignKey(ForSome, on_delete=models.CASCADE,null=True,blank=True)
    lab                     =           models.ForeignKey(Labs, on_delete=models.CASCADE,null=True,blank=True)
    amount                  =           models.FloatField(default=0)
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
    report                  =           models.FileField(max_length=100,blank=True,null=True,default="")
    desc                    =           models.CharField(max_length=50,blank=True,null=True,default="")
    send_to_doctor          =           models.BooleanField(default=False)
    is_active               =           models.BooleanField(default=False)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ['-updated_at']

    @staticmethod
    def give_slot_details(id):
        instance = Slot.objects.filter(id=id).first()        
        data = {}
        data['booking_id'] = instance.id
        data['amount'] = instance.amount
        data['status'] = instance.status
        progress_pecentage = 0
        if instance.status == "":
            progress_pecentage = 20
        if instance.status == "accepted":
            progress_pecentage = 50
        if instance.status == "taken":
            progress_pecentage = 100
        if instance.status == "rejected":
            progress_pecentage = 100

        data['progress'] = progress_pecentage
        return data


@receiver(post_save, sender=Slot)
def slot_status_handler(sender,instance,created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {}
        data['booking_id'] = instance.id
        data['amount'] = instance.amount
        data['status'] = instance.status

        progress_pecentage = 0
        if instance.status == "":
            progress_pecentage = 20
        if instance.status == "accepted":
            progress_pecentage = 50
        if instance.status == "taken":
            progress_pecentage = 100
        if instance.status == "rejected":
            progress_pecentage = 100

        data['progress'] = progress_pecentage

        async_to_sync(channel_layer.group_send)(
            'booking_%s' % instance.id,{
                'type' : 'slot_status',
                'value' : json.dumps(data)
            }
        )

class PicturesForMedicine(models.Model):
    id                      =           models.AutoField(primary_key=True)
    patient                 =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    prescription            =           models.FileField(upload_to=None, max_length=256,default="",blank=True,null=True)
    store_invoice           =           models.FileField(upload_to=None, max_length=256,default="",blank=True,null=True)
    pharmacy                =           models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    amount                  =           models.FloatField(default=0,blank=True,null=True)
    amount_paid             =           models.BooleanField(default=False)
    applied_date            =           models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True,max_length=64)
    applied_time            =           models.TimeField(auto_now=False, auto_now_add=False,blank=True,null=True,max_length=64)
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
    desc                    =           models.CharField(max_length=50,blank=True,null=True,default="")
    is_active               =           models.BooleanField(default=False)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ['-created_at']

    @staticmethod
    def give_picture_details(id):
        instance = PicturesForMedicine.objects.filter(id=id).first()        
        data = {}
        data['booking_id'] = instance.id
        data['amount'] = instance.amount
        data['status'] = instance.status
        data['amount_paid'] = instance.amount_paid
        data['invoice'] = str(instance.store_invoice)

        progress_pecentage = 0
        if instance.status == "":
            progress_pecentage = 20
        elif instance.status == "accepted":
            progress_pecentage = 40
        elif instance.store_invoice:
            progress_pecentage = 60
        elif instance.amount_paid:
            progress_pecentage = 80
        elif instance.status == "taken":
            progress_pecentage = 100
        elif instance.status == "rejected":
            progress_pecentage = 100

        data['progress'] = progress_pecentage
        return data

@receiver(post_save, sender=PicturesForMedicine)
def pictureformedicine_status_handler(sender,instance,created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {}
        data['booking_id'] = instance.id
        data['amount'] = instance.amount
        data['status'] = instance.status
        data['amount_paid'] = instance.amount_paid
        data['invoice'] = instance.store_invoice

        progress_pecentage = 0
        if instance.status == "":
            progress_pecentage = 20
        elif instance.status == "accepted":
            progress_pecentage = 40
        elif instance.store_invoice:
            progress_pecentage = 60
        elif instance.amount_paid:
            progress_pecentage = 80
        elif instance.status == "taken":
            progress_pecentage = 100
        elif instance.status == "rejected":
            progress_pecentage = 100

        data['progress'] = progress_pecentage

        async_to_sync(channel_layer.group_send)(
            'booking_%s' % instance.id,{
                'type' : 'pictureformedicine_status',
                'value' : json.dumps(data,default=str)
            }
        )

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

    class Meta:
        ordering = ['-created_at']

class patientFile(models.Model):
    id                      =           models.AutoField(primary_key=True)
    treatmentreliefpetient  =           models.ForeignKey(TreatmentReliefPetient, on_delete=models.CASCADE)
    booking                 =           models.ForeignKey(Booking, on_delete=models.CASCADE,null=True)
    patient                 =           models.ForeignKey(Patients, on_delete=models.CASCADE,null=True)
    hospitaldoctors         =           models.ForeignKey(HospitalStaffDoctors, on_delete=models.CASCADE,null=True)
    amount_paid             =           models.FloatField()
    file                    =           models.FileField(upload_to="patients/documents/fiel/%Y/%m/%d/",blank=True,null=True,default="")
    # file_date               =           models.DateField(blank=True,null=True)
    # file_time               =           models.TimeField(blank=True,null=True)
    file_purpose            =           models.CharField(default="",blank=True,null=True,max_length=500)
    file_addnote            =           models.TextField(default="",blank=True,null=True,max_length=5000)
    is_active               =           models.BooleanField(default=False)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ['-created_at']

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

    class Meta:
        ordering = ['-created_at']

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

    class Meta:
        ordering = ['-created_at']

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

class Temp(models.Model):
    id                      =          models.AutoField(primary_key=True)
    user                    =          models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_id                =          models.IntegerField()
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()

class LabTest(models.Model):
    id                      =           models.AutoField(primary_key=True)
    lab                     =           models.ForeignKey(Labs, on_delete=models.CASCADE)
    service                 =           models.ForeignKey(ServiceAndCharges, on_delete=models.CASCADE)
    slot                    =           models.ForeignKey(Slot, on_delete=models.CASCADE)
    is_active               =           models.BooleanField(default=False)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()
    
    class Meta:
        ordering = ['-created_at']

class Orders(models.Model):
    id                      =           models.AutoField(primary_key=True)
    patient                 =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service                 =           models.ForeignKey(ServiceAndCharges, on_delete=models.CASCADE)
    bookingandlabtest       =           models.CharField(max_length=50,default="",blank=True,null=True)
    BOOKING_FOR_CHOICE      =           ((1,"Hospital"),(2,"Laboratory"),(3,"Pharmacy"))
    booking_for             =           models.CharField(max_length=256,default="",blank=True,null=True,choices=BOOKING_FOR_CHOICE)
    amount                  =           models.FloatField(default=0,blank=True,null=True)
    STATUS_TYPE_CHOICE      =           ((1,"Processed"),(2,"Successed"),(3,"Failed"),(4,"Cancelled"),(5,"Refunded"))
    status                  =           models.CharField(default="",blank=True,null=True,max_length=64,choices=STATUS_TYPE_CHOICE)    
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    is_booking_Verified     =           models.BooleanField(default=False)
    is_taken                =           models.BooleanField(default=False)
    counter                 =           models.IntegerField(default=0, blank=False)
    taken_date_time         =           models.DateTimeField(blank=True,null=True,auto_now=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ['-created_at']

class phoneOPTforoders(models.Model):
    id =  models.AutoField(primary_key=True)
    order_id =  models.ForeignKey(Orders,  on_delete=models.CASCADE,null=True,blank=True)
    user =  models.ForeignKey(CustomUser,  on_delete=models.CASCADE,null=True,blank=True)
    otp      =  models.CharField(max_length=50,null=True,blank=True,default="")
    count      =  models.IntegerField(null=True,blank=True,default=0)
    validated      =  models.BooleanField(null=True,blank=True,default=False)
    otp_session_id  = models.CharField(max_length=50,null=True,blank=True,default=None)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)


