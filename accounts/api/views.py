from django.shortcuts import render,get_object_or_404, redirect
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from accounts.utils import generate_token
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from django.http import HttpResponse,JsonResponse
import http.client
import json
# import requests
import ast
import random
from django.contrib.auth import authenticate,login,logout
from django.utils.encoding import force_bytes

import lab

from .serializers import DProfilePropertiesSerializer, HProfilePropertiesSerializer, LProfilePropertiesSerializer, PHProfilePropertiesSerializer, PProfilePropertiesSerializer, RegistrationSerializer,AccountPropertiesSerializer,ChangePasswordSerializer #ProfilePropertiesSerializer

from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView)
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes

from rest_framework import status,permissions

from accounts.models import AdminHOD, CustomUser, DoctorForHospital, Hospitals, Labs,Patients, Pharmacy,PhoneOTP
from accounts.EmailBackEnd import EmailBackEnd

from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import (
	AllowAny,
	)
from rest_framework.authtoken.models import Token

from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

conn = http.client.HTTPConnection("2factor.in")





class ValidatePhoneSendOTP(APIView):

    authentication_classes = []
    permission_classes = []
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        # password = request.data.get('password', False)
        # username = request.data.get('username', False)
        # email    = request.data.get('email', False)
        print(phone_number)
        # permission_classes = [IsAuthenticated]
        if phone_number:
            phone = str(phone_number)
            user = CustomUser.objects.filter(phone__iexact = phone)			
            # if user.exists():
            #     return Response({
            #         'status' : False,
            #         'detail' : 'Phone number already exists'
            #     })

            # else:
            key = send_otp(phone)
            if key:
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        old.otp=key
                        if count > 10:
                            return Response({
                                'status' : False,
                                'detail' : 'Sending otp error. Limit Exceeded. Please Contact Customer support'
                            })

                        old.count = count +1
                        old.save()
                        print('Count Increase', count)

                        #conn.request("GET", "https://2factor.in/API/V1/f08f2dc9-aa1a-11eb-80ea-0200cd936042/SMS/"+phone+"/"+str(key))

                        # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042"+phone+"&otpvalue="+str(key)+"&templatename=WomenMark1")
                        # conn.request("GET", "http://dnd.saakshisoftware.in/api/mt/SendSMS?user=Sect&password=Sect@123&senderid=GLOBAL&channel=Promo&DCS=0&flashsms=0&number=91989xxxxxxx&text=test message&route=##&DLTTemplateId=approvded dlt templateid&PEID=sender entity id")
                        #res = conn.getresponse() 
                       
                        #data = res.read()
                        #data=data.decode("utf-8")
                        #data=ast.literal_eval(data)
                        
                        
                        #if data["Status"] == 'Success':
                         #   old.otp_session_id = data["Details"]
                          #  old.save()
                            # print('In validate phone :'+old.otp_session_id)
                        return Response({
                                  'status' : True,
                                   'detail' : 'OTP sent successfully',
								    'opt' : key,
                                })    
                        # else:
                        #     return Response({
                        #           'status' : False,
                        #           'detail' : 'OTP sending Failed'
                        #         }) 
                   
                    else:
                        print(phone,key)
                        obj=PhoneOTP.objects.create(
                            phone=phone,
                            otp = key,
                        )
                        # conn.request("GET", "https://2factor.in/API/V1/f08f2dc9-aa1a-11eb-80ea-0200cd936042/SMS/"+phone+"/"+str(key))
                        # res = conn.getresponse()    
                        # data = res.read()
                        # print(data.decode("utf-8"))
                        # data=data.decode("utf-8")
                        # data=ast.literal_eval(data)

                        # if data["Status"] == 'Success':
                        #     obj.otp_session_id = data["Details"]
                        #     print(obj)
                        #     obj.save()
                            # print('In validate phone :'+obj.otp_session_id)
                        return Response({
                                   'status' : True,
                                   'detail' : 'OTP sent successfully',
								   'opt' : key,
                                })    
                        # else:
                        #     return Response({
                        #           'status' : False,
                        #           'detail' : 'OTP sending Failed'
                        #         })

                       
            else:
                return Response({
                        'status' : False,
                        'detail' : 'Sending otp error'
                })   

        else:
            return Response({
                'status' : False,
                'detail' : 'Phone number is not given in post request'
            })            

def send_otp(phone):
    if phone:
        key = random.randint(999,9999)
        print(key)
        return key
    else:
        return False

class ValidateOTP(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        data = {}
        if phone and otp_sent:
            print(phone)
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                print(otp_sent,old.otp)
                if otp_sent == old.otp:
                    # data["Status"] = 'success'
                	
                # print("In validate otp"+otp_session_id)
                # conn.request("GET", "http://2factor.in/API/V1/f08f2dc9-aa1a-11eb-80ea-0200cd936042/SMS/VERIFY/"+otp_session_id+"/"+otp_sent)
                # res = conn.getresponse()    
                # data = res.read()
                # print(data.decode("utf-8"))
                # data=data.decode("utf-8")
                # data=ast.literal_eval(data)
                # if data["Status"] == 'Success':
                    old.validated = True
                    old.otp_session_id = "bkjbjbkkj"
                    print(old)
                    old.save()
                    return Response({
                        'status' : True,
                        'detail' : 'OTP MATCHED. Please proceed for registration.'
                            })

                else:
                    return Response({
                        'status' : False,
                        'detail' : 'OTP INCORRECT'
                    })
                


            else:
                return Response({
                        'status' : False,
                        'detail' : 'First Proceed via sending otp request'
                    })


        else:
            return Response({
                        'status' : False,
                        'detail' : 'Please provide both phone and otp for Validation'
                    })

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):

	if request.method == 'POST':
		data = {}
		email = request.data.get('email', '0').lower()
		if validate_email(email) != None:
			data['error_message'] = 'That email is already in use.'
			data['response'] = 'Error'
			return Response(data)

		username = request.data.get('username', '0')
		if validate_username(username) != None:
			data['error_message'] = 'That username is already in use.'
			data['response'] = 'Error'
			return Response(data)

		phone = request.data.get('phone', '0')
		if validate_phone(phone) != None:
			data['error_message'] = 'That phone is already in use.'
			data['response'] = 'Error'
			return Response(data)
		
		old = PhoneOTP.objects.filter(phone__iexact = phone)
		old = old.first()
		if old.validated:
			serializer = RegistrationSerializer(data=request.data)
		
			if serializer.is_valid():
				account = serializer.save(request)
				data['response'] = 'successfully registered new user.'
				data['email'] = account.email
				data['username'] = account.username
				data['phone'] = account.phone
				data['pk'] = account.pk
				token = Token.objects.get(user=account).key
				data['token'] = token
				# user = Customers.objects.filter(admin = request.user)
				# user.phone = account.phone
				
				old.delete()

			else:
				data = serializer.errors
			return Response(data)
			# return Response(
            #             {'status' : True,
            #             'detail' : 'Account Created Successfully'}
            #             )   		
		else:
			return Response(data,
				{
				'status' : False,
				'detail' : 'OTP havent Verified. First do that Step.'
				}
			)

def validate_email(email):
	account = None
	try:
		account = CustomUser.objects.get(email=email)
	except CustomUser.DoesNotExist:
		return None
	if account != None:
		return email

def validate_phone(phone):
	account = None
	try:
		account = CustomUser.objects.get(phone=phone)
	except CustomUser.DoesNotExist:
		return None
	if account != None:
		return phone

def validate_username(username):
	account = None
	try:
		account = CustomUser.objects.get(username=username)
	except CustomUser.DoesNotExist:
		return None
	if account != None:
		return username

class AccountProperpertiesView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	def get(self, request):
		try:
			account = request.user
			print("succes")
		except CustomUser.DoesNotExist:
			print("fialed")
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		serializer = AccountPropertiesSerializer(account)
		return Response(serializer.data)
		
class AccountProperpertiesUpdateView(UpdateAPIView):
	serializer_class = AccountPropertiesSerializer
	model = CustomUser
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	def put(self, request):
		try:
			account = request.user
			print("succes")
		except CustomUser.DoesNotExist:
			print("fialed")
			return Response(status=status.HTTP_404_NOT_FOUND)
			
		serializer = AccountPropertiesSerializer(account,data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = "Account Updated Successfully"
			return Response(data=data)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ProfileProperpertiesView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	def get(self, request):
		try:
			if request.user.user_type == "1":
				account = AdminHOD.objects.get(admin=request.user)
				print("admin")				
			if request.user.user_type == "2":
				account = Hospitals.objects.get(admin=request.user)
				print("hospital")
			if request.user.user_type == "3":
				account = DoctorForHospital.objects.get(admin=request.user)
				print("doctor")
			if request.user.user_type == "4":
				account = Patients.objects.get(admin=request.user)
				print("patient")
			if request.user.user_type == "5":
				account = Labs.objects.get(admin=request.user)
				print("labs")
			if request.user.user_type == "6":
				account = Pharmacy.objects.get(admin=request.user)
				print("pahrmacy")			
		except CustomUser.DoesNotExist:
			print("fialed")
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		if request.user.user_type == "2":
			serializer = HProfilePropertiesSerializer(account)
		if request.user.user_type == "3":
			serializer = DProfilePropertiesSerializer(account)
		if request.user.user_type == "4":
			serializer = PProfilePropertiesSerializer(account)
		if request.user.user_type == "5":
			serializer = LProfilePropertiesSerializer(account)
		if request.user.user_type == "6":
			print("pahrmacy")
			serializer = PHProfilePropertiesSerializer(account)

		return Response(serializer.data)

class ProfileProperpertiesUpdateView(UpdateAPIView):
	serializer_class = AccountPropertiesSerializer
	model = CustomUser
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	def put(self, request):
		try:
			if request.user.user_type == "1":
				account = AdminHOD.objects.get(admin=request.user)
			if request.user.user_type == "2":
				account = Hospitals.objects.get(admin=request.user)
			if request.user.user_type == "3":
				account = DoctorForHospital.objects.get(admin=request.user)
			if request.user.user_type == "4":
				account = Patients.objects.get(admin=request.user)
			if request.user.user_type == "5":
				account = Labs.objects.get(admin=request.user)
			if request.user.user_type == "6":
				account = Pharmacy.objects.get(admin=request.user)
			print("succes")
		except CustomUser.DoesNotExist:
			print("fialed")
			return Response(status=status.HTTP_404_NOT_FOUND)

		if request.user.user_type == "2":
			serializer = HProfilePropertiesSerializer(account,data=request.data)
		if request.user.user_type == "3":
			serializer = DProfilePropertiesSerializer(account,data=request.data)
		if request.user.user_type == "4":
			serializer = PProfilePropertiesSerializer(account,data=request.data)
		if request.user.user_type == "5":
			serializer = LProfilePropertiesSerializer(account,data=request.data)
		if request.user.user_type == "6":
			serializer = PHProfilePropertiesSerializer(account,data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = "Account Updated Successfully"
			return Response(data=data)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ObtainAuthTokenView(APIView):

	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}

		email = request.POST.get('username')
		password = request.POST.get('password')
		account = EmailBackEnd.authenticate(request,username=email, password=password)
		if account:
			try:
				token = Token.objects.get(user=account)
			except Token.DoesNotExist:
				token = Token.objects.create(user=account)
			if account.is_active == True:
				context['response'] = 'Successfully authenticated.'
				context['pk'] = account.pk
				context['email'] = account.email.lower()
				context['phone'] = account.phone
				context['username'] = account.username
				context['token'] = token.key
			else:
				context['response'] = 'Error'
				context['error_message'] = 'Check you email for activte account'
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'

		return Response(context)

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def does_account_exist_view(request):

	if request.method == 'POST':
		email = request.POST['email'].lower()
		data = {}
		try:
			account = CustomUser.objects.get(email=email)
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
			data['response'] = "Email Exists"
			data['email_send'] = "YES"
		except CustomUser.DoesNotExist:
			data['response'] = "Account does not exist"
			data['email_send'] = "NO"
		return Response(data,status=status.HTTP_200_OK)

class ChangePasswordView(UpdateAPIView):

	serializer_class = ChangePasswordSerializer
	model = CustomUser
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	def get_object(self, queryset=None):
		obj = self.request.user
		return obj

	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			# Check old password
			if not self.object.check_password(serializer.data.get("old_password")):
				return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

			# confirm the new passwords match
			new_password = serializer.data.get("new_password")
			confirm_new_password = serializer.data.get("confirm_new_password")
			if new_password != confirm_new_password:
				return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

			# set_password also hashes the password that the user will get
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			return Response({"response":"successfully changed password"}, status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CustomerRegister(CreateAPIView):
	# 	permission_classes = (AllowAny,)

	# 	serializer_class = CustomerRegisterSerializer

	# 	queryset = CustomUser.objects.all()
		
	# class InstructorRegister(CreateAPIView):
	# 	permission_classes = (AllowAny,)

	# 	serializer_class = InstructorRegisterSerializer
	# 	queryset = CustomUser.objects.all()


	# @api_view(['GET',])
	# @permission_classes((IsAuthenticated,))
	# def account_properties_view(request):
	# 	try:
	# 		account = request.user
	# 	except CustomUser.DoesNotExist:
	# 		return Response(status=status.HTTP_404_NOT_FOUND)

	# 	if request.method == 'GET':
	# 		serializer = AccountPropertiesSerializer(account)
	# 		return Response(serializer.data)

	# @api_view(['POST',])
	# def CustomerRegister(request):
		
	# 	if request.method == "POST":
	# 		serializer = CustomerRegisterSerializer(data=request.data)
	# 		data = {}
	# 		if serializer.is_valid():
	# 			user_obj = serializer.save(request)
	# 			data['response'] = "successfully Registered a new user"
	# 			data['email'] = user_obj.email
	# 			data['username'] = user_obj.username
	# 			token = Token.objects.get(user=user_obj).key
	# 			data['token'] = token
	# 		else:
	# 			data = serializer.errors
	# 		return Response(data) 

	# @api_view(['POST',])
	# def InstructorRegister(request):
		
	# 	if request.method == "POST":
	# 		serializer = InstructorRegisterSerializer(data=request.data)
	# 		data = {}
	# 		if serializer.is_valid():
	# 			user_obj = serializer.save(request)
	# 			data['response'] = "successfully Registered a new user"
	# 			data['email'] = user_obj.email
	# 			data['username'] = user_obj.username
	# 			token = Token.objects.get(user=user_obj).key
	# 			data['token'] = token
	# 		else:
	# 			data = serializer.errors
	# 		return Response(data) 

	# @api_view(['PUT',])
	# @permission_classes((IsAuthenticated,))
	# def update_account_view(request):
	# 	try:
	# 		account = request.user
	# 	except CustomUser.DoesNotExist:
	# 		return Response(status=status.HTTP_404_NOT_FOUND)
		
	# 	if request.method == 'PUT':
	# 		serializer = AccountPropertiesSerializer(account,data=request.data)
	# 		data = {}
	# 		if serializer.is_valid():
	# 			serializer.save()
	# 			data['response'] = "Account Updated Successfully"
	# 			return Response(data=data)
	# 		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


	# @api_view(['GET',])
	# @permission_classes((IsAuthenticated,))
	# def profile_properties_view(request):
	# 	try:
	# 		account = Patients.objects.get(admin=request.user)
	# 		print(account)
	# 	except Patients.DoesNotExist:
	# 		return Response(status=status.HTTP_404_NOT_FOUND)

	# 	if request.method == 'GET':
	# 		serializer = ProfilePropertiesSerializer(account)
	# 		return Response(serializer.data)