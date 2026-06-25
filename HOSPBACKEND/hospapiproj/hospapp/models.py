from django.db import models

# Create your models here.

# Patient model
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), 
                                                      ('female', 'Female'), 
                                                      ('other', 'Other')])
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name

# Department model
class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.department_name

# Doctor model
class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    doctor_name = models.CharField(max_length=100)
    prompt = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='doctors')
    
    def __str__(self):
        return self.doctor_name

# Consultation model
class Consultation(models.Model):
    consultation_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), 
                                                      ('completed', 'Completed')])
    created_at = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='consultations')

    def __str__(self):
        return f"{self.patient.patient_name} - {self.doctor.doctor_name}"

# ChatMessage model
class ChatMessage(models.Model):
    chat_id = models.AutoField(primary_key=True)
    sender = models.CharField(max_length=20, choices=[('patient', 'Patient'), 
                                                      ('doctor', 'Doctor')])
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return self.sender

# MedicalImage model
class MedicalImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='medical_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    analysis = models.TextField(blank=True, null=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image {self.image_id} for Consultation {self.consultation.consultation_id}"

# Prescription model
class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    diagnosis = models.TextField()
    medicines = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='prescriptions')

    def __str__(self):
        return f"Prescription {self.prescription_id}"
