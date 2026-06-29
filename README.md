# 🏥 AstraClinicAI

An AI-powered virtual healthcare consultation platform that enables patients to interact with AI specialist doctors through text-based conversations and medical image analysis. The system generates AI-assisted medical guidance and prescriptions using Google Gemini 2.5 Flash.

> **Note**: This application is intended for educational purposes and provides preliminary medical guidance. It is not a replacement for professional medical advice.

## TECH STACK

Streamlit (Frontend)

Django Rest (Backend)

MySQL (Database)

Google Gemini 2.5 flash (AI)

## 🏗 System Architecture

Patient

   │
   
   ▼
   
Streamlit Frontend

   │
   
REST API

   │
   
Django REST Framework

   │
   
 ├── MySQL Database
 
 └── Google Gemini 2.5 Flash

 ## 🔄 Workflow

1. Patient registers or logs into the system.
2. Patient selects an AI specialist.
3. A consultation session is created.
4. Patient chats with the AI doctor.
5. Patient can upload a medical image.
6. Gemini analyzes both the conversation and the uploaded image.
7. AI provides healthcare guidance.
8. AI generates a prescription.
9. Consultation ends and patient returns to the dashboard.
 

