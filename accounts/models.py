from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db import models
from django.db.models.fields import AutoField
from django.db.models.signals import post_save
from django.dispatch import receiver
# from ckeditor_uploader.fields import RichTextUploadingField
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.core.validators import RegexValidator
from django.db.models import Q
# Create your models here.

# class CustomUser(AbstractUser): 
#     user_type_data=((1,"HOD"),(2,"Staff"),(3,"Customer"))
#     user_type=models.CharField(choices=user_type_data,max_length=10)

class MyAccountManager(BaseUserManager):
    # create _create_user for mobiel number for facebbook and for google and for userid password so it can be solve your all problem regarding social login/auth
    use_in_migrations = True
    def create_user(self, email, username,password=None):
        if not email:
            raise ValueError("User must have an Email Address")
        if not username:
            raise ValueError("User must have an username ")

        user = self.model(
                email=self.normalize_email(email),
                username=username,                
               
            )
        user.is_active= False
        user.set_password(password)
        user.save(using=self._db)
        print(user)

        return user

    def create_superuser(self, email, username, password,**extra_fields):
        user = self.create_user(
                email=self.normalize_email(email),
                password=password,
                username=username,                           
                
            )
        
        # phone = "7801925101"
        user.is_active = True
        # user.is_admin = True
        # user_type="0"
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser): 
    email = models.EmailField(verbose_name="email", max_length=254, unique=True,error_messages={'unique':"This email has already been registered."})
    username = models.CharField(max_length=254,unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True,null=True,blank=True)
    last_login = models.DateTimeField(verbose_name="date joined" ,auto_now_add=True,null=True,blank=True)
    # is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    name_title   =models.CharField(max_length=256,blank=True,null=True,default="")
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    user_type_data=((1,"AdminHOD"),(2,"Hospitals"),(3,"HospitalDoctors"),(4,"Patients"),(5 ,"Labs"),(6 ,"Pharmacy"))
    user_type=models.CharField(choices=user_type_data,max_length=50)
    phone_regex     = RegexValidator( regex = r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format +919999999999. Up to 10 digits allowed.")
    phone           = models.CharField('Phone',validators =[phone_regex], max_length=10, unique = True,null=True)
    is_Mobile_Verified      = models.BooleanField(blank=False, default=False)
    is_Email_Verified      = models.BooleanField(blank=False, default=False)
    counter         = models.IntegerField(default=0, blank=False) #OTP counter
    otp_session_id  = models.CharField(max_length=120, null=True, default = "")
    profile_pic         =models.FileField(upload_to="user/profile_pic",max_length=500,null=True,default="")
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_superuser

    def has_module_perms(self,app_label):
        return True    

class PhoneOTP(models.Model):
    
    # id=models.AutoField(primary_key=True)
    # admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    phone_regex     = RegexValidator( regex = r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format +919999999999. Up to 14 digits allowed.")
    phone           = models.CharField(validators =[phone_regex], max_length=17, unique = True)
    otp             = models.CharField(max_length=9, blank = True, null=True)
    count           = models.IntegerField(default=0, help_text = 'Number of otp_sent')
    validated       = models.BooleanField(default = False, help_text = 'If it is true, that means user have validate otp correctly in second API')
    otp_session_id  = models.CharField(max_length=120, null=True, default = "")
    username        = models.CharField(max_length=20, blank = True, null = True, default = None )
    email           = models.CharField(max_length=50, null = True, blank = True, default = None) 
    password        = models.CharField(max_length=100, null = True, blank = True, default = None) 

    

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)   

class AdminHOD(models.Model):
    id                  =models.AutoField(primary_key=True)
    admin               =models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects             =models.Manager()

class Hospitals(models.Model):
    id                  =models.AutoField(primary_key=True)
    admin               =models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    hopital_name        =models.CharField(max_length=500,default="",null=True)
    about               =models.TextField(blank=True,null=True,default="")
    # registration_number =models.DateField(blank=True,null=True,default="")
    address1             =models.CharField(max_length=500,blank=True,null=True,default="")
    address2             =models.CharField(max_length=500,blank=True,null=True,default="")
    city                =models.CharField(max_length=50,blank=True,null=True,default="")
    pin_code            =models.CharField(max_length=50,blank=True,null=True,default="")
    state               =models.CharField(max_length=50,blank=True,null=True,default="")
    country             =models.CharField(max_length=50,blank=True,null=True,default="")
    landline            =models.CharField(max_length=50,blank=True,null=True,default="")
    SPECIALIST_TYPE_CHOICE=((1,"PHYSICIAN"),(2,"SURGEN"),(3,"CARDIOLOGY"),(4,"NEUROLOGISTS"))
    specialist          =models.CharField(max_length=256,blank=True,null=True,default="",choices=SPECIALIST_TYPE_CHOICE)
    profile_pic         =models.FileField(upload_to="Hospital/profile/images/%Y/%m/%d/",max_length=500,null=True,default="")
    is_appiled          =models.BooleanField(blank=True,null=True,default=False)
    is_verified         =models.BooleanField(blank=True,null=True,default=False)
    is_deactive         =models.BooleanField(blank=True,null=True,default=False)
    registration_proof  =models.FileField(upload_to="hospital/documents/images/%Y/%m/%d/", max_length=500,blank=True,null=True,default="")
    establishment_year  =models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    registration_number =models.CharField(max_length=50,blank=True,null=True,default="")
    alternate_mobile    =models.CharField(max_length=50,blank=True,null=True,default="")
    website             =models.URLField(max_length=256,blank=True,null=True,default="")
    linkedin            =models.URLField(max_length=256,blank=True,null=True,default="")
    facebook            =models.URLField(max_length=256,blank=True,null=True,default="")
    instagram           =models.URLField(max_length=256,blank=True,null=True,default="")
    twitter             =models.URLField(max_length=256,blank=True,null=True,default="")
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects             =models.Manager()
    
    def __str__(self):
        return self.hopital_name  

class HospitalPhones(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="")
    hospital_mobile     =models.CharField(max_length=256,blank=True,null=True,default="")
    hospital_email      =models.CharField(max_length=256,blank=True,null=True,default="")
    is_active           =models.BooleanField(default=False)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)

class Patients(models.Model):
    id                  =models.AutoField(primary_key=True)
    admin               =models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    fisrt_name          =models.CharField(max_length=250,blank=True,null=True,default="")
    last_name           =models.CharField(max_length=250,blank=True,null=True,default="")
    address             =models.CharField(max_length=500,blank=True,null=True,default="")
    city                =models.CharField(max_length=250,blank=True,null=True,default="")
    state               =models.CharField(max_length=250,blank=True,null=True,default="")
    country             =models.CharField(max_length=250,blank=True,null=True,default="")
    zip_Code            =models.CharField(max_length=250,blank=True,null=True,default="")
    dob                 =models.DateField(blank=True,null=True)
    alternate_mobile    =models.CharField(max_length=250,blank=True,null=True,default="")
    profile_pic         =models.FileField(upload_to="patients/profile/images/%Y/%m/%d/",blank=True,null=True,default="")
    gender              =models.CharField(max_length=255,null=True,default="")
    bloodgroup          =models.CharField(max_length=255,null=True,default="")
    is_appiled          =models.BooleanField(blank=True,null=True,default=False)
    is_verified         =models.BooleanField(blank=True,null=True,default=False)
    is_active           =models.BooleanField(blank=True,null=True,default=False)
    created_at          =models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at          =models.DateTimeField(auto_now_add=True,null=True,blank=True)
    objects             =models.Manager()
    
    def __str__(self): 
        return self.fisrt_name +" "+ self.last_name

class HospitalDoctors(models.Model):
    id                  =models.AutoField(primary_key=True)
    # admin               =models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name_title          =models.CharField(max_length=256,blank=True,null=True,default="")
    fisrt_name          =models.CharField(max_length=250,blank=True,null=True,default="")
    last_name           =models.CharField(max_length=250,blank=True,null=True,default="")
    address             =models.CharField(max_length=500,blank=True,null=True,default="")
    city                =models.CharField(max_length=250,blank=True,null=True,default="")
    state               =models.CharField(max_length=250,blank=True,null=True,default="")
    country             =models.CharField(max_length=250,blank=True,null=True,default="")
    zip_Code            =models.CharField(max_length=250,blank=True,null=True,default="")
    phone               =models.CharField(max_length=50,default="",blank=True,null=True)
    degree              =models.CharField(max_length=50,default="",blank=True,null=True)
    specialist          =models.CharField(max_length=50,default="",blank=True,null=True)
    dob                 =models.DateField(blank=True,null=True,default="")
    alternate_mobile    =models.CharField(max_length=250,blank=True,null=True,default="")
    profile_pic         =models.FileField(upload_to="Doctor/profile/images/%Y/%m/%d/",blank=True,null=True)
    gender              =models.CharField(max_length=255,null=True,default="")
    linkedin            =models.URLField(max_length=256,blank=True,null=True,default="")
    facebook            =models.URLField(max_length=256,blank=True,null=True,default="")
    instagram           =models.URLField(max_length=256,blank=True,null=True,default="")
    is_appiled          =models.BooleanField(blank=True,null=True,default=False)
    is_verified         =models.BooleanField(blank=True,null=True,default=False)
    created_at          =models.DateTimeField(auto_now=True,blank=True,null=True)
    updated_at          =models.DateTimeField(auto_now_add=True,blank=True,null=True)
    objects             =models.Manager()
    
    def __str__(self):
        return self.fisrt_name +" "+ self.last_name

class Labs(models.Model):
    id                  =models.AutoField(primary_key=True)
    admin               =models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    lab_name            =models.CharField(max_length=500,default="",null=True)
    about                =models.TextField(max_length=5000,default="",null=True)
    registration_number =models.CharField(max_length=50,blank=True,null=True,default="")
    address             =models.CharField(max_length=500,blank=True,null=True,default="")
    pin_code            =models.CharField(max_length=250,blank=True,null=True,default="")
    city                =models.CharField(max_length=50,blank=True,null=True,default="")
    state               =models.CharField(max_length=50,blank=True,null=True,default="")
    country             =models.CharField(max_length=50,blank=True,null=True,default="")
    landline            =models.CharField(max_length=50,blank=True,null=True,default="")
    specialist          =models.CharField(max_length=256,blank=True,null=True,default="")
    profile_pic         =models.FileField(upload_to="hospital/profile/images/%Y/%m/%d/",max_length=500,null=True,default="")
    is_appiled          =models.BooleanField(blank=True,null=True,default=False)
    is_deactive         =models.BooleanField(blank=True,null=True,default=False)
    is_verified         =models.BooleanField(blank=True,null=True,default=False)
    registration_proof  =models.FileField(upload_to="hospital/documents/images/%Y/%m/%d/", max_length=500,blank=True,null=True,default="")
    establishment_year  =models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    website             =models.URLField(max_length=256,blank=True,null=True,default="")
    linkedin            =models.URLField(max_length=256,blank=True,null=True,default="")
    facebook            =models.URLField(max_length=256,blank=True,null=True,default="")
    instagram           =models.URLField(max_length=256,blank=True,null=True,default="")
    twitter             =models.URLField(max_length=256,blank=True,null=True,default="")
    contact_person      =models.CharField(max_length=256,blank=True,null=True,default="")
    alternate_mobile    =models.CharField(max_length=50,blank=True,null=True,default="")
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects             =models.Manager()
    
    def __str__(self):
        return self.lab_name  

class Pharmacy(models.Model):
    id                  =models.AutoField(primary_key=True)
    admin               =models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    pharmacy_name       =models.CharField(max_length=500,default="",null=True)
    registration_number =models.CharField(max_length=50,blank=True,null=True,default="")
    address             =models.CharField(max_length=500,blank=True,null=True,default="")
    pin_code            =models.CharField(max_length=250,blank=True,null=True,default="")
    city                =models.CharField(max_length=50,blank=True,null=True,default="")
    state               =models.CharField(max_length=50,blank=True,null=True,default="")
    country             =models.CharField(max_length=50,blank=True,null=True,default="")
    landline            =models.CharField(max_length=50,blank=True,null=True,default="")
    specialist          =models.CharField(max_length=256,blank=True,null=True,default="")
    profile_pic         =models.FileField(upload_to="Pharmacist/profile/images/%Y/%m/%d/",max_length=500,null=True,default="")
    about               =models.TextField(max_length=5000,blank=True,null=True,default="")
    is_appiled          =models.BooleanField(blank=True,null=True,default=False)
    is_deactive         =models.BooleanField(blank=True,null=True,default=False)
    is_verified         =models.BooleanField(blank=True,null=True,default=False)
    registration_proof  =models.FileField(upload_to="Pharmacist/documents/images/%Y/%m/%d/", max_length=500,blank=True,null=True,default="")
    establishment_year  =models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    website             =models.URLField(max_length=256,blank=True,null=True,default="")
    linkedin             =models.URLField(max_length=256,blank=True,null=True,default="")
    facebook            =models.URLField(max_length=256,blank=True,null=True,default="")
    instagram           =models.URLField(max_length=256,blank=True,null=True,default="")
    twitter             =models.URLField(max_length=256,blank=True,null=True,default="")
    contact_person      =models.CharField(max_length=256,blank=True,null=True,default="")
    alternate_mobile    =models.CharField(max_length=50,blank=True,null=True,default="")
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects             =models.Manager()
    
    def __str__(self):
        return self.pharmacy_name  

class UserPayments(models.Model):
    id                  =models.AutoField(primary_key=True)
    patient             =models.ForeignKey(Patients, on_delete=models.CASCADE)
    payment_type        =models.CharField(max_length=50)
    payment_provider    =models.CharField(max_length=50)
    account_info        =models.IntegerField()
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)

class DoctorForHospital(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    doctor              =models.ForeignKey(HospitalDoctors, on_delete=models.CASCADE)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects             =models.Manager()
     
    def __str__(self):
        return self.hospital.hospital_name


class OPDTime(models.Model):
    id                      =           models.AutoField(primary_key=True)
    user                    =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    opening_time            =           models.TimeField(max_length=500,blank=True,null=True)
    close_time              =           models.TimeField(max_length=500,blank=True,null=True)
    break_start_time        =           models.TimeField(max_length=500,blank=True,null=True)
    break_end_time          =           models.TimeField(max_length=500,blank=True,null=True)
    monday                              =models.CharField(max_length=500,default="",blank=True,null=True) 
    tuesday                             =models.CharField(max_length=500,default="",blank=True,null=True) 
    wednesday                           =models.CharField(max_length=500,default="",blank=True,null=True) 
    thursday                            =models.CharField(max_length=500,default="",blank=True,null=True) 
    friday                              =models.CharField(max_length=500,default="",blank=True,null=True) 
    saturday                            =models.CharField(max_length=500,default="",blank=True,null=True) 
    sunday                              =models.CharField(max_length=500,default="",blank=True,null=True)
    is_active               =           models.BooleanField(blank=True,null=True,default=False)
    created_at              =           models.DateTimeField(auto_now=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()
    

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Hospitals.objects.create(admin=instance)
            OPDTime.objects.create(user=instance)
        if instance.user_type==3:
            HospitalDoctors.objects.create(admin=instance)
            OPDTime.objects.create(user=instance)
        if instance.user_type==4:
            Patients.objects.create(admin=instance)            
        if instance.user_type==5:
            Labs.objects.create(admin=instance)
            OPDTime.objects.create(user=instance)
        if instance.user_type==6:
            Pharmacy.objects.create(admin=instance)
            OPDTime.objects.create(user=instance)

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.hospitals.save()
    if instance.user_type==3:
        instance.hospitaldoctors.save()
    if instance.user_type==4:
        instance.patients.save()        
    if instance.user_type==5:
        instance.labs.save()
    if instance.user_type==6:
        instance.pharmacy.save()