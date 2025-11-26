from django import forms
from .models import Disease

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ['title', 'description']
        labels = {
            'title': 'Krankheit / Diagnose',
            'description': 'Behandlungsplan / Beschreibung',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': ''}),
        }
