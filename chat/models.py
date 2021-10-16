import channels
from django.db import models
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