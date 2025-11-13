from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm





class RegistroUsuario(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        