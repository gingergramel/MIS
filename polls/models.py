from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Practitioner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    office_hours = models.TextField()
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    insurance_number = models.CharField(max_length=20)
    practitioner = models.ForeignKey('Practitioner', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Questionnaire(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    
    # Hauptbeschwerde als Multiple-Choice
    MAIN_COMPLAINT_CHOICES = [
        ('RUECKEN', 'Rückenschmerzen'),
        ('KOPF', 'Kopfschmerzen'),
        ('GELENK', 'Gelenkschmerzen'),
        ('SONSTIGES', 'Sonstiges'),
    ]
    main_complaint = models.CharField(max_length=20, choices=MAIN_COMPLAINT_CHOICES, blank=True, null=True)
    
    # Schmerzanamnese
    pain_duration = models.CharField(max_length=200, verbose_name='Wie lange haben Sie die Beschwerden schon?', null=True, blank=True)
    pain_frequency = models.CharField(max_length=200, verbose_name='Wie oft treten die Beschwerden auf?', null=True, blank=True)
    pain_intensity = models.CharField(max_length=200, verbose_name='Wie stark sind die Beschwerden?', null=True, blank=True)
    previous_treatment = models.CharField(max_length=200, verbose_name='Wurden Sie wegen dieser Beschwerden schon behandelt?', null=True, blank=True)

    def __str__(self):
        return f"Fragenkatalog von {self.patient}" 

class Message(models.Model):
   
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='messages')
    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender_is_practitioner = models.BooleanField(default=False)
    read_by_practitioner = models.BooleanField(default=False)
    read_by_patient = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        sender = 'Practitioner' if self.sender_is_practitioner else 'Patient'
        return f"{sender} message ({self.patient} <-> {self.practitioner})"

class Disease(models.Model):
    practitioner = models.ForeignKey('Practitioner', on_delete=models.CASCADE, related_name='diseases')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='diseases')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.patient.user.first_name} {self.patient.user.last_name})"