from rest_framework import serializers
from .models import Patient, Department, Doctor, Consultation, ChatMessage, MedicalImage, Prescription

# Patient serializer
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

# Department serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

# Doctor serializer
class DoctorSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Doctor
        fields = '__all__'

# Consultation serializer
class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'

# ChatMessage serializer
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

# MedicalImage serializer
class MedicalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalImage
        fields = '__all__'

# Prescription serializer
class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'  
