from rest_framework import routers
from .views import PatientViewSet, DepartmentViewSet, DoctorViewSet, ConsultationViewSet, ChatMessageViewSet, MedicalImageViewSet, PrescriptionViewSet
from django.urls import path
from .views import test_gemini


router = routers.DefaultRouter()

router.register(r'patients', PatientViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'consultations', ConsultationViewSet)
router.register(r'chatmessages', ChatMessageViewSet)
router.register(r'medicalimages', MedicalImageViewSet)
router.register(r'prescriptions', PrescriptionViewSet)

urlpatterns = router.urls + [
    path(
        'test-gemini/',
        test_gemini,
        name='test-gemini'
    ),
]