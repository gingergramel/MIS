"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from polls import views as pmapp_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pmapp_views.home, name='home'),
    path('patient/login/', pmapp_views.patient_login, name='patient_login'),
    path('practitioner/login/', pmapp_views.practitioner_login, name='practitioner_login'),
    path('logout/', pmapp_views.perform_logout, name='logout'),
    path('patient/register/', pmapp_views.patient_register, name='patient_register'),
    path('practitioner/register/', pmapp_views.practitioner_register, name='practitioner_register'),
    path('register/', pmapp_views.perform_register, name='register'),
    path('questionnaire/', pmapp_views.questionnaire, name='questionnaire'),
    path('practitioner_dashboard/', pmapp_views.practitioner_dashboard, name='practitioner_dashboard'),
    path('patient_dashboard/', pmapp_views.patient_dashboard, name='patient_dashboard'),
    path('edit_profile/', pmapp_views.edit_profile, name='edit_profile'),
    path('patient/messages/', pmapp_views.patient_messages, name='patient_messages'),
    path('practitioner/messages/<int:patient_id>/', pmapp_views.view_patient_messages, name='view_patient_messages'),
    path('add_disease/<int:patient_id>/', pmapp_views.add_disease_for_patient, name='add_disease'),
    path('view_disease/', pmapp_views.view_disease, name='view_disease'),
]
