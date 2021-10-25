from django.http import request
from rest_framework import serializers
from rest_framework.serializers import (
	ModelSerializer,
	ValidationError,
	EmailField,
	CharField,
)
import accounts
from accounts.models import CustomUser,Hospitals,DoctorForHospital,HospitalDoctors,Patients,Labs,Pharmacy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from accounts.utils import generate_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError




class RegistrationSerializer(serializers.ModelSerializer):

	# password2 				= serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = CustomUser
		fields = ['email', 'username', 'password', 'phone','user_type']
		extra_kwargs = {
				'password': {'write_only': True},
		}	
	
	
	def	save(self,request):
		username = self.validated_data['username']
		password = self.validated_data['password']
		phone = self.validated_data['phone']
		email = self.validated_data['email']
		user_type = self.validated_data['user_type']
		# if password != password_2:
		# 	raise serializers.ValidationError({'password':'password does not match'})
		account = CustomUser.objects.create_user(username=username,password=password,email=email)
		account.user_type=user_type
		account.phone=phone
		account.is_active = True
		if user_type == "2":
			patient = Hospitals()
			patient.admin = account
			patient.save()
		if user_type == "3":
			patient = DoctorForHospital()
			patient.admin = account
			patient.save()
		if user_type == "4":
			patient = Patients()
			patient.admin = account
			patient.save()
		if user_type == "5":
			patient = Labs()
			patient.admin = account
			patient.save()
		if user_type == "6":
			patient = Pharmacy()
			patient.admin = account
			patient.save()		
		account.save()
		
		print("serializer line 47")
		current_site=get_current_site(request)
		# current_site="127.0.0.1:8000"
		email_subject='Active your Account',
		message=render_to_string('accounts/activate.html',
		{
			'user':account,
			'domain':current_site.domain,
			# 'domain':"127.0.0.1:8000",
			'uid':urlsafe_base64_encode(force_bytes(account.pk)),
			'token':generate_token.make_token(account)
		}
		)	
		email_message=EmailMessage(
			email_subject,
			message,
			settings.EMAIL_HOST_USER,
			[email]
		)
		email_message.send()
		return account

class AccountPropertiesSerializer(serializers.ModelSerializer):

	class Meta:
		model = CustomUser
		fields = ['name_title','first_name','last_name','is_Mobile_Verified','is_Email_Verified','profile_pic','pk', 'email', 'username', 'phone',]

class ChangePasswordSerializer(serializers.Serializer):

	old_password 				= serializers.CharField(required=True)
	new_password 				= serializers.CharField(required=True)
	confirm_new_password 		= serializers.CharField(required=True)


class PProfilePropertiesSerializer(serializers.ModelSerializer):

	class Meta:
		model = Patients
		fields = "__all__"

class HProfilePropertiesSerializer(serializers.ModelSerializer):

	class Meta:
		model = Hospitals
		fields = "__all__"

class LProfilePropertiesSerializer(serializers.ModelSerializer):

	class Meta:
		model = Labs
		fields = "__all__"

class PHProfilePropertiesSerializer(serializers.ModelSerializer):

	class Meta:
		model = Pharmacy
		print("pahrmacy")
		fields = "__all__"

class DProfilePropertiesSerializer(serializers.ModelSerializer):

	class Meta:
		model = DoctorForHospital
		fields = "__all__"


# class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta: 
#         model = CustomUser 
#         fields = ('email','username','password','user_type_data')



# class CustomerRegisterSerializer(ModelSerializer):
# 	password2 = CharField(style={'input_type':'password'},write_only=True)
# 	email = EmailField(label='Email adress')
# 	class Meta:
# 		model = CustomUser
# 		fields = [
# 			'id',
# 			'username',
# 			'password',
# 			'password2',
# 			'email',           
# 		]
# 	extra_kwargs = {"password":
# 					{"write_only":True},
# 					"id":
# 					{"read_only":True}
# 					}

# 	def validate(self, data):
# 		return data

# 	def validate_email(self, value):
# 		email = value
# 		user_qs = CustomUser.objects.filter(email=email)
# 		if user_qs.exists():
# 			raise ValidationError("Email alredy registred")
# 		return value
 
# 	def save(self, request):
# 		username = self.validated_data['username']
# 		password = self.validated_data['password']
# 		password_2 = self.validated_data['password2']
# 		email = self.validated_data['email']
# 		user_type = "3"
		# if password != password_2:
		# 	raise serializers.ValidationError({'password':'password does not match'})
# 		user_obj = CustomUser.objects.create_user(username=username,password=password,email=email,user_type=3)
# 		user_obj.is_active = False
# 		user_obj.save()
# 		current_site=get_current_site(request)
# 		# current_site="127.0.0.1:8000"
# 		email_subject='Active your Account',
# 		message=render_to_string('accounts/activate.html',
# 		{
# 			'user':user_obj,
# 			'domain':current_site.domain,
# 			# 'domain':"127.0.0.1:8000",
# 			'uid':urlsafe_base64_encode(force_bytes(user_obj.pk)),
# 			'token':generate_token.make_token(user_obj)
# 		}
# 		)	
# 		email_message=EmailMessage(
# 			email_subject,
# 			message,
# 			settings.EMAIL_HOST_USER,
# 			[email]
# 		)
# 		email_message.send()
# 		return user_obj
 		 
# class InstructorRegisterSerializer(ModelSerializer):
# 	password2 = CharField(style={'input_type':'password'},write_only=True)
# 	email = EmailField(label='Email adress')
# 	class Meta:
# 		model = CustomUser
# 		fields = [
# 			'id',
# 			'username',
# 			'password',
# 			'password2',
# 			'email',            
# 		]
# 	extra_kwargs = {"password":
# 					{"write_only":True},
# 					"id":
# 					{"read_only":True}
# 					}

# 	def validate(self, data):
# 		return data

# 	def validate_email(self, value):
# 		email = value
# 		user_qs = CustomUser.objects.filter(email=email)
# 		if user_qs.exists():
# 			raise ValidationError("Email alredy registred")
# 		return value

# 	def save(self, request):
# 		username = self.validated_data['username']
# 		password = self.validated_data['password']
# 		password_2 = self.validated_data['password2']
# 		email = self.validated_data['email']
# 		if password != password_2:
# 			raise serializers.ValidationError({'password':'password does not match'})
# 		user_obj = CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
# 		user_obj.is_active = False		
# 		user_obj.save()
# 		current_site=get_current_site(request)
# 		# current_site="127.0.0.1:8000"
# 		email_subject='Active your Account',
# 		message=render_to_string('accounts/activate.html',
# 		{
# 			'user':user_obj,
# 			'domain':current_site.domain,
# 			# 'domain':"127.0.0.1:8000",
# 			'uid':urlsafe_base64_encode(force_bytes(user_obj.pk)),
# 			'token':generate_token.make_token(user_obj)
# 		}
# 		)	
# 		email_message=EmailMessage(
# 			email_subject,
# 			message,
# 			settings.EMAIL_HOST_USER,
# 			[email]
# 		)
# 		email_message.send()
# 		return user_obj

# class AcccountPropertiesSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = CustomUser
# 		fields = ['pk','email','username',]
	
# class ProfilePropertiesSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = Customers
# 		fields = ['fisrt_name','last_name','dob','address','city','state','country','phone','gender','photo','qualification',]

# class ChangePasswordSerializer(serializers.Serializer):

# 	old_password 				= serializers.CharField(required=True)
# 	new_password 				= serializers.CharField(required=True)
# 	confirm_new_password 		= serializers.CharField(required=True)