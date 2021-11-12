from django.contrib import admin

from patient.models import Booking, ForSome, ReBooking,phoneOPTforoders,Orders,LabTest,Temp,patientFile,PatientBottelAndInjections,PatientMedicine,PatientReports,PatientSymptons,PicturesForMedicine,TreatmentReliefPetient,Admited,FollowedUp,Slot,ReBooking,ForSome
# Register your models here.

admin.site.register(Booking)
admin.site.register(ForSome)
admin.site.register(ReBooking)
admin.site.register(Admited)
admin.site.register(FollowedUp)
admin.site.register(Slot)
admin.site.register(PicturesForMedicine)
admin.site.register(TreatmentReliefPetient)
admin.site.register(patientFile)
admin.site.register(PatientSymptons)
admin.site.register(PatientReports)
admin.site.register(PatientMedicine)
admin.site.register(PatientBottelAndInjections)
admin.site.register(Temp)
admin.site.register(LabTest)
admin.site.register(Orders)
admin.site.register(phoneOPTforoders)