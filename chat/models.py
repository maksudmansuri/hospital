import channels
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from accounts.models import CustomUser
from patient.models import Booking, PicturesForMedicine, Slot
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
# Create your models here.


class Notification(models.Model):
    id       =           models.AutoField(primary_key=True)
    # 1= appointment,  2 = comment, 3 = feedback, 4 = others , 5= report , 6 = message
    notification_type =           models.IntegerField()
    to_user =    models.ForeignKey(CustomUser,related_name="notification_to", on_delete=models.CASCADE,null=True)
    from_user =  models.ForeignKey(CustomUser,related_name="notification_from", on_delete=models.CASCADE,null=True)
    booking =    models.ForeignKey(Booking,related_name="hospitalbooking", on_delete=models.CASCADE,null=True,blank=True)
    slot =       models.ForeignKey(Slot,related_name="labs", on_delete=models.CASCADE,null=True,blank=True)
    picturesmedicine = models.ForeignKey(PicturesForMedicine,related_name="picturesmedicine", on_delete=models.CASCADE,null=True,blank=True)
    user_has_seen  =           models.BooleanField(default=False)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ['-created_at']


    def save(self,*args, **kwargs):
        channels_layer = get_channel_layer()
        notification_objs = Notification.objects.filter(user_has_seen=False).count()
        data = {'count' : notification_objs, 'current_notification':self.booking.status}

        async_to_sync(channels_layer.group_send)(
            'test_consumer_group',{
                'type' : 'send_notification',
                'value' : json.dumps(data)
            }

        ) 
        super(Notification,self).save(*args, **kwargs)
    
    # @staticmethod
    # def give_notification_details(id):
    #     instance = Notification.objects.filter(to_user=id).first()
    #     data = {}
    #     data['id'] = instance.id
    #     data['from_user'] = instance.from_user.id
    #     data['notification_type'] = instance.notification_type
    #     if instance.booking:
    #         data['booking'] = instance.booking.id
    #     else:
    #         data['booking'] = ""
    #     if instance.slot:
    #         data['slot'] = instance.slot.id
    #     else:
    #         data['slot'] = ""
    #     if instance.picturesmedicine:
    #         data['picturesmedicine'] = instance.picturesmedicine.id
    #     else:
    #         data['picturesmedicine'] = ""
    #     data['user_has_seen'] = instance.user_has_seen
    #     return data

@receiver(post_save, sender=Notification)
def notification_handler(sender, instance, created,**kwargs):
    print(instance)
    if created:
        channel_layer = get_channel_layer()
        data = {}
        data['id'] = instance.id
        data['from_user_profile_pic'] = str(instance.from_user.profile_pic)
        data['from_user_user_type'] = instance.from_user.user_type
        print("signal called 2")
        if instance.notification_type == "1": # this is for appoinment  
            if instance.from_user.user_type =="1": #radmin
                data['name'] = instance.from_user.patients.fisrt_name + " " + instance.from_user.patients.last_name 
            elif instance.from_user.user_type =="2": #Hospital
                data['name'] = instance.from_user.hospitals.hospital_name
            elif instance.from_user.user_type =="3": # DOctor
                data['name'] = instance.from_user.hospitals.Doctor_name
            elif instance.from_user.user_type =="4":#patient
                data['name'] = instance.from_user.patients.fisrt_name + " " + instance.from_user.patients.last_name
            elif instance.from_user.user_type =="5":#lab
                data['name'] = instance.from_user.labs.labs_name
            elif instance.from_user.user_type =="6":#pharmacy
                data['name'] = instance.from_user.pharmacy.pharmacy_name
            print("signal called 2.1")
            if instance.booking:
                if instance.booking.booking_type == "OPD":
                    data['booking'] = "For OPD"
                if instance.booking.booking_type == "Emergency":
                    data['booking'] = "For Emergency"
                if instance.booking.booking_type == "ONLINE":
                    data['booking'] = "For Online"
                if instance.booking.booking_type == "HOME":
                    data['booking'] = "For Home Visit"
            elif instance.slot:
                    data['booking'] = "For Lab Test"                
            elif instance.picturesmedicine:
                    data['booking'] = "New Order"
        print("signal called 3")
        print(instance.to_user)
        async_to_sync(channel_layer.group_send)(
            'notificaion_%s' % instance.to_user.id,{
                'type' : 'send_notification',
                'value' : json.dumps(data)
            }
        )
    
