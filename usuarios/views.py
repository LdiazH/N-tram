from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistroUsuario
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.urls import reverse_lazy

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password) #Verifica si el usuario existe en la base de datos
        if usuario is not None:
            login(request, usuario) #Crea la sesión del usuario
            return redirect('home') #Redirige a la página de inicio
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)# funcion hecha de moedelo auth que elimina la sesion actual
    return redirect('login')

class RegistroUsuario(CreateView):
    template_name = 'registro.html'
    form_class = RegistroUsuario
    success_url = reverse_lazy('registro_exitoso')