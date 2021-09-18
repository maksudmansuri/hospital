from accounts.models import CustomUser
from django.db import models

# Create your models here.
class Medias(models.Model):
    id                      =           models.AutoField(primary_key=True)
    user                    =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    media_type              =           models.CharField(max_length=255,blank=True,null=True,default="")
    media_type_choice       =           ((1,"Image"),(2,"Video"))
    media_content           =           models.FileField(choices=media_type_choice,blank=True,null=True,default="")
    media_desc              =           models.CharField(max_length=255,blank=True,null=True,default="")
    is_active               =           models.BooleanField(default=False)     
    is_default              =           models.BooleanField(default=False)     
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    