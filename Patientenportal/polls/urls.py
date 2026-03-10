from django.urls import path
from . import views

urlpatterns = [
    # Startseite
    path('', views.home, name='home'),

    # Authentifizierung & Registrierung
    path('patient/login/', views.patient_login, name='patient_login'),
    path('patient/register/', views.patient_register, name='patient_register'),
    path('practitioner/login/', views.practitioner_login, name='practitioner_login'),
    path('practitioner/register/', views.practitioner_register, name='practitioner_register'),

    # Dashboards
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('practitioner/dashboard/', views.practitioner_dashboard, name='practitioner_dashboard'),

    # Profile & Fragebogen
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),

    # Nachrichten
    path('patient/messages/', views.patient_messages, name='patient_messages'),
    path('practitioner/messages/<int:patient_id>/', views.view_patient_messages, name='view_patient_messages'),
]
