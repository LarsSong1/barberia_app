# En barberia/forms.py

from django import forms
from .models import Barberia
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class BarberiaForm(forms.ModelForm):
    class Meta:
        model = Barberia
        fields = ['imagen', 'titulo', 'descripcion', 'ubicacion', 'numero_contacto', 'maps', 'insta']
    
    def __init__(self, *args, **kwargs):
        super(BarberiaForm, self).__init__(*args, **kwargs)
     
        self.fields['imagen'].widget.attrs.update({'class': 'file-input w-full max-w-xs'})
        self.fields['titulo'].widget.attrs.update({'class': 'bg-white border-2 border-black rounded-sm text-black'})
        self.fields['descripcion'].widget.attrs.update({'class': 'bg-white border-2 border-black rounded-sm text-black'})
        self.fields['ubicacion'].widget.attrs.update({'class': 'bg-white border-2 border-black rounded-sm text-black'})
        self.fields['numero_contacto'].widget.attrs.update({'class': 'bg-white border-2 border-black rounded-sm text-black'})

        



class CustomUserCreationForm(UserCreationForm):
    TYPE_CHOICES = [
        ('Barbero', 'Barbero'),
        ('Cliente', 'Cliente'),
    ]

    tipo_usuario = forms.ChoiceField(choices=TYPE_CHOICES, required=True, help_text='Seleccione el tipo de usuario')

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('tipo_usuario',)

