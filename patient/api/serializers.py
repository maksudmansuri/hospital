from django.db.models import fields
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from accounts.models import  DoctorForHospital, HospitalDoctors, Hospitals, Labs
from hospital.models import HospitalStaffDoctors, ServiceAndCharges
from patient import models
from patient.models import Booking, LabTest, Orders, PicturesForMedicine, Slot



class HospitalsSerializer(serializers.ModelSerializer):

	# username = serializers.SerializerMethodField('get_username_from_staffs')
	# product_image = serializers.SerializerMethodField('validate_product_image_url')

	class Meta: 
		model = Hospitals
		fields ="__all__"

	# def get_username_from_staffs(self,Product):
	# 	username = Hospitals.admin
	# 	return username

	def validate_product_image_url(self, Product):
		crs_imge = Hospitals.admin.profile_pic
		new_url = crs_imge.url
		if "?" in new_url:
			new_url = crs_imge.url[:crs_imge.url.rfind("?")]
		return new_url

class DoctorDetailSerialzer(serializers.ModelSerializer):

	class Meta:
		model = HospitalDoctors
		fields = "__all__"	

class HospitalDoctorSerialzer(serializers.ModelSerializer):

	class Meta:
		model = HospitalStaffDoctors
		fields = ['id','email','ssn_id','opd_charges','home_charges','emergency_charges','joindate','is_virtual_available','is_online','is_active','created_at','updated_at']
		
	def to_representation(self, instance):
		response = super().to_representation(instance)
		print(instance)
		response['doctor_extra'] = DoctorDetailSerialzer(instance.doctor).data
		return response

class HospitalDoctorsViewSerializer(serializers.ModelSerializer):
	hospitalstaffdoctors = HospitalDoctorSerialzer(many=True)	
	
	class Meta:
		model = Hospitals
		fields = ['hopital_name','about','address1','address2','city','pin_code','state','country','landline','specialist','profile_pic','registration_proof','establishment_year','registration_number','alternate_mobile','firm','website','linkedin','facebook','instagram','twitter','created_at','updated_at','hospitalstaffdoctors']

class OnlineDoctorserializer(serializers.ModelSerializer):

	class Meta:
		model = HospitalStaffDoctors
		fields = '__all__'

"""
Appointment Serializers
"""
class ServicesSerializer(serializers.ModelSerializer):

	class Meta:
		model = ServiceAndCharges
		fields = "__all__"

class HospitalForBookingSerializer(serializers.ModelSerializer):

	class Meta:
		model = Booking
		fields = "__all__"
	
	def to_representation(self, instance):
		response = super().to_representation(instance)
		response['service_name'] = ServicesSerializer(instance.service).data
		return response

class LabTestserializer(serializers.ModelSerializer):

	class Meta:
		model = LabTest
		fields = "__all__"

	def to_representation(self, instance):
		response = super().to_representation(instance)
		response['service_name'] = ServicesSerializer(instance.service).data
		return response

class LabsForBookingserializer(serializers.ModelSerializer):
	labtest = LabTestserializer(many=True)

	class Meta:
		model = Slot
		fields = ['id','patient','for_whom','lab','amount','applied_date','applied_time','is_applied','status','accepted_date','taken_date','rejected_date','is_rejected','is_taken','is_accepted','is_cancelled','modified_time','modified_date','add_note','report','desc','send_to_doctor','is_active','created_at','updated_at','labtest']
			
class PharmacyForBookingserializer(serializers.ModelSerializer):

	class Meta:
		model = PicturesForMedicine
		fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Orders
		fields = ['id','patient','service','bookingandlabtest','booking_for','amount','status','created_at','updated_at','is_cancelled','is_booking_Verified','is_taken','counter','taken_date_time']

	def to_representation(self, instance):
		response = super().to_representation(instance)
		print(instance.booking_for)
		if instance.booking_for == "1":
			booking = get_object_or_404(Booking,id=int(instance.bookingandlabtest))
			print(booking)
			response['booking'] = HospitalForBookingSerializer(booking).data
		if instance.booking_for == "2":
			slot = get_object_or_404(Slot,id=int(instance.bookingandlabtest))
			response['slot'] = LabsForBookingserializer(slot).data
		if instance.booking_for == "3":
			pictureformedicine = get_object_or_404(PicturesForMedicine,id=int(instance.bookingandlabtest))
			response['pictureformedicine'] = PharmacyForBookingserializer(pictureformedicine).data
		return response

"""
Labs serializers
"""

class LabsViewSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Labs
		fields = '__all__'
	
"""
Pharmacy serializers
"""
class PharmacysViewSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Labs
		fields = '__all__'
	

	