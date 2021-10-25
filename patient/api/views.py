
from django.contrib.auth import models
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Hospitals, Labs, Pharmacy
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter

from hospital.models import HospitalStaffDoctors
from patient.models import Orders

from .serializers import AppointmentSerializer, HospitalDoctorSerialzer, HospitalDoctorsViewSerializer, HospitalsSerializer, LabsViewSerializer, OnlineDoctorserializer, PharmacysViewSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

class ApiHospitalListView(ListAPIView):
	queryset = Hospitals.objects.all()
	serializer_class = HospitalsSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter,OrderingFilter)
	search_fields = ('hopital_name','specialist','city')

class ApiHospitalListAndDetailsView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter,OrderingFilter)
	search_fields = ('hopital_name','specialist','city')

	def get(self, request, id=None):
		# print(request.data['id'])		
		if id:
			hospital = get_object_or_404(Hospitals,id = id,is_verified = True,admin__is_active = True)
			# hospitaldoctors = HospitalStaffDoctors.objects.filter(hospital=hospital)
			# serializer = HospitalDoctorsViewSerializer(hospitalDoctors)
			# return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
			serializer = HospitalDoctorsViewSerializer(hospital)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		hospital = Hospitals.objects.all()
		serializer = HospitalsSerializer(hospital, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class HospitalDoctorDetailsView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)


	def get(self,request,id=None,did=None):
		if id and did:
			print(id,did)
			hospital = get_object_or_404(Hospitals,id=id,is_verified=True,admin__is_active = True)
			print(hospital)
			hospitaldoctors = HospitalStaffDoctors.objects.get(id=did,hospital=hospital,is_active=True)
			print(hospitaldoctors)
			
			serializer = HospitalDoctorSerialzer(hospitaldoctors)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class APIOnlineDoctorListView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	def get(self,request,id=None,did=None):
		if id:
			hospitaldoctors = HospitalStaffDoctors.objects.get(id=id,is_active=True,is_virtual_available=True)			
			serializer = OnlineDoctorserializer(hospitaldoctors)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		hospitaldoctors = HospitalStaffDoctors.objects.filter(is_virtual_available=True,is_active=True)
		serializer = OnlineDoctorserializer(hospitaldoctors, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class APIHomevisitDoctorListView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	def get(self,request,id=None,did=None):
		if id:
			hospitaldoctors = HospitalStaffDoctors.objects.get(id=id,is_active=True,is_homevisit_available=True)			
			serializer = OnlineDoctorserializer(hospitaldoctors)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		hospitaldoctors = HospitalStaffDoctors.objects.filter(is_homevisit_available=True,is_active=True)
		serializer = OnlineDoctorserializer(hospitaldoctors, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


"""
LAbs Views
"""

class ApiLabsListAndDetailsView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter,OrderingFilter)
	search_fields = ('lab_name','specialist','city')

	def get(self, request, id=None):
		if id:
			lab = get_object_or_404(Labs,id = id,is_verified = True,admin__is_active = True)
			serializer = HospitalLabsViewSerializer(lab)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		labs = Labs.objects.all()
		serializer = LabsViewSerializer(labs, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

"""
Pharmacy Views
"""

class ApiPharmacyListAndDetailsView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter,OrderingFilter)
	search_fields = ('lab_name','specialist','city')

	def get(self, request, id=None):
		if id:
			pharmacy = get_object_or_404(Pharmacy,id = id,is_verified = True,admin__is_active = True)
			serializer = PharmacysViewSerializer(pharmacy)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		pharmacy = Pharmacy.objects.all()
		serializer = PharmacysViewSerializer(pharmacy, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

"""
Appointment Views
"""
class AppointmentListView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	def get(self,request,id=None):
		if id:
			order = Orders.objects.get(id=id)			
			serializer = AppointmentSerializer(order)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		orders = Orders.objects.filter( patient  = request.user )
		serializer = AppointmentSerializer(orders, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


