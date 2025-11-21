from django import forms
from .models import Reserva
from django.utils import timezone

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['rut', 'fecha_inicio']
        widgets = {
            'rut': forms.TextInput(attrs={'placeholder': '12345678-9'}),
            'fecha_inicio': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'value': timezone.now().strftime('%Y-%m-%dT%H:%M')
                }
            ),
        }
        labels = {
            'rut': 'RUT del reservante',
            'fecha_inicio': 'Fecha y Hora de Inicio',
        }
    
    def __init__(self, *args, sala=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.sala = sala
    
    def clean(self):
        cleaned_data = super().clean()
        
        if self.sala:
            if not self.sala.habilitada:
                raise forms.ValidationError("Esta sala no está habilitada para reservas")
            
            if not self.sala.disponible:
                raise forms.ValidationError("Esta sala ya está reservada")
        
        return cleaned_data
    
    def save(self, commit=True):
        reserva = super().save(commit=False)
        reserva.sala = self.sala
        if commit:
            reserva.save()
        return reserva