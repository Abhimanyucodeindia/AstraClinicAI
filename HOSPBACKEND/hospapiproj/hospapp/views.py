from PIL import Image
import os
from google import genai
from dotenv import load_dotenv
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PatientSerializer, DepartmentSerializer, DoctorSerializer, ConsultationSerializer, ChatMessageSerializer, MedicalImageSerializer, PrescriptionSerializer
from .models import Patient, Department, Doctor, Consultation, ChatMessage, MedicalImage, Prescription

#===============================================================================
# GEMINI AI INITIALISATION & AUTHENTICATION
# load environment variables from .env file
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
#===============================================================================

# Test gemini response
@api_view(['GET'])
def test_gemini(request):

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="What is Django?"
        )

        return Response({
            "response": response.text
        })

    except Exception as e:

        return Response({
            "error": str(e)
        })
    
#===============================================================================

# Create your views here.
# Patient viewset
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

# Department viewset
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

# Doctor viewset
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    
    # used to get doctors by department using the department id
    @action(                                         #-------> CUSTOM API
        detail=False,
        methods=['get'],
        url_path=r'department/(?P<dept_id>\d+)'
    )
    def by_department(self, request, dept_id):
        doctors = Doctor.objects.filter(department_id=dept_id)
        serializer = self.get_serializer(
            doctors,
            many=True
        )
        return Response(serializer.data)
    
#===============================================================================
# Consultation viewset
class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

    # used to send and store 
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):

        consultation = self.get_object()

        message = request.data.get("message")
        if not message:
            return Response(
                {"error":"Message is required"},
                status=400
            )
        # Save patient message
        ChatMessage.objects.create(
            consultation=consultation,
            sender="PATIENT",
            message=message
        )

        doctor = consultation.doctor

        # Get all messages of this consultation
        messages = consultation.messages.order_by(
            "-timestamp"
        )[:20]

        messages = reversed(messages)

        # Build conversation history
        history = ""

        for msg in messages:

            history += (
                f"{msg.sender}: "
                f"{msg.message}\n"
            )

        # Create final prompt
        full_prompt = f"""
        {doctor.prompt}

        You are consulting a patient.

        Conversation History:
        {history}

        If an image is attached,
        analyze it together with the symptoms.

        Do not claim certainty.
        Provide possible observations and advice.

        Respond as a professional doctor.
        """
        # Gemini response
        
        latest_image = consultation.images.order_by(
            "-uploaded_at"
            ).first()

        if latest_image:

            image = Image.open(
                latest_image.image.path
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    full_prompt,
                    image
                ]
            )

        else:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
        ai_response = response.text

        # Save AI response
        ChatMessage.objects.create(
            consultation=consultation,
            sender="doctor",
            message=ai_response
        )

        return Response({
            "response": ai_response
        })
    
    # used to generate PRESCRIPTION
    @action(detail=True, methods=['post'])
    def generate_prescription(self, request, pk=None):

        consultation = self.get_object()

        doctor = consultation.doctor

        messages = consultation.messages.order_by(
            "timestamp"
        )

        history = ""

        for msg in messages:

            history += (
                f"{msg.sender}: "
                f"{msg.message}\n"
            )

        prompt = f"""
        {doctor.prompt}

        Based on the conversation below generate:

        Diagnosis:
        Medicines:
        Instructions:

        Return only in this format:

        Diagnosis: <text>

        Medicines: <text>

        Instructions: <text>

        Conversation:
        {history}
        """

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            prescription_text = response.text

            diagnosis = ""
            medicines = ""
            instructions = ""

            lines = prescription_text.split("\n")

            current_section = None

            for line in lines:

                if line.startswith("Diagnosis:"):

                    current_section = "diagnosis"

                    diagnosis += (
                        line.replace(
                            "Diagnosis:",
                            ""
                        ).strip()
                    )

                elif line.startswith("Medicines:"):

                    current_section = "medicines"

                    medicines += (
                        line.replace(
                            "Medicines:",
                            ""
                        ).strip()
                    )

                elif line.startswith("Instructions:"):

                    current_section = "instructions"

                    instructions += (
                        line.replace(
                            "Instructions:",
                            ""
                        ).strip()
                    )

                else:

                    if current_section == "diagnosis":

                        diagnosis += (
                            "\n" + line
                        )

                    elif current_section == "medicines":

                        medicines += (
                            "\n" + line
                        )

                    elif current_section == "instructions":

                        instructions += (
                            "\n" + line
                        )

            prescription = Prescription.objects.create(
                consultation=consultation,
                diagnosis=diagnosis.strip(),
                medicines=medicines.strip(),
                instructions=instructions.strip()
            )

            return Response({

                "prescription_id":
                prescription.prescription_id,

                "diagnosis":
                diagnosis,

                "medicines":
                medicines,

                "instructions":
                instructions

            })

        except Exception as e:

            return Response({
                "error": str(e)
            })
#===============================================================================

# ChatMessage viewset
class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

# MedicalImage viewset
class MedicalImageViewSet(viewsets.ModelViewSet):
    queryset = MedicalImage.objects.all()
    serializer_class = MedicalImageSerializer
    # used 
    @action(detail=True, methods=['post'])# Open image file path using Pillow
    def analyze(self, request, pk=None):
    # 💡 HINT: This action uses Gemini 2.5 Flash (Vision) to analyze an uploaded 

        # skin image. It saves the AI's structural observations directly to the 

        # database but explicitly avoids giving a definitive medical diagnosis.

        # 🛠️ REQUIREMENT: Needs 'Pillow' installed (pip install pillow) for Image.open().
        medical_image = self.get_object()

        try:
            # Open image file path using Pillow
            image = Image.open(
                medical_image.image.path
            )

            # Call Gemini Multimodal API
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    """
                    You are an AI Dermatologist.

                    Analyze the uploaded skin image.

                    Provide:
                    1. Possible observations
                    2. Possible conditions
                    3. General advice

                    Do not provide a final diagnosis.
                    """,
                    image
                ]
            )

            analysis = response.text

            # Save the analysis result back to this image instance
            medical_image.analysis = analysis
            medical_image.save()

            return Response({
                "analysis": analysis
            })

        except Exception as e:

            return Response({
                "error": str(e)
            })

# Prescription viewset
class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer



