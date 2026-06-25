from django.contrib import admin
from .models import Patient, Department, Doctor, Consultation, ChatMessage, MedicalImage, Prescription
# Register your models here.

admin.site.register(Patient)
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Consultation)
admin.site.register(ChatMessage)
admin.site.register(MedicalImage)
admin.site.register(Prescription)