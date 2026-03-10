from django.contrib import admin
from .models import Patient, Practitioner, Questionnaire

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'insurance_number', 'practitioner')
    list_filter = ('practitioner',)
    search_fields = ('user__username', 'insurance_number')
    fields = ('user', 'date_of_birth', 'address', 'phone_number', 'insurance_number', 'practitioner')

admin.site.register(Patient, PatientAdmin)
admin.site.register(Practitioner)
admin.site.register(Questionnaire)
