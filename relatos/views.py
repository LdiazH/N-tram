from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import ListView, CreateView, DetailView, TemplateView, DeleteView, UpdateView

from .forms import RelatoForm
from django.urls import reverse_lazy

#importacion del formualrio de registro


#importacion del modelo Relato y categoria
from .models import Relato, Categoria

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'   

 
class NoPermiso(TemplateView):
    template_name = 'no_permiso.html'
    
class RegistroExitoso(TemplateView):
    template_name = 'registro_exitoso.html'
 
#vista publica de los relatos    
class ListaRelatosView(ListView):
    model = Relato
    template_name = 'lista_relatos.html'
    context_object_name = 'relatos'
    ordering = ['-created_at']
    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_id = self.request.GET.get('categoria')

        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        categoria_id = self.request.GET.get('categoria')

        if categoria_id:
            context['categoria_seleccionada'] = Categoria.objects.get(id=categoria_id)
        else:
            context['categoria_seleccionada'] = None

        return context

#Creador relato    
class RelatoCreateView(LoginRequiredMixin, CreateView):
    model = Relato
    form_class = RelatoForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('relatos')
    
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)
  
# Detalle relato  
class RelatoDetailView(DetailView):
    model = Relato
    template_name = "detalle_relato.html"
    context_object_name = "relato"
    
#  Editar relato 
class RelatoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Relato
    form_class = RelatoForm
    template_name = 'formulario.html'  # puedes usar el mismo que el create
    success_url = reverse_lazy('relatos')

    def test_func(self):
        relato = self.get_object()
        return self.request.user == relato.autor
    

# Eliminar relato 
class RelatoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Relato
    template_name = "confirmar_eliminacion.html"
    success_url = reverse_lazy('relatos')

    def test_func(self):
        relato = self.get_object()
        return self.request.user == relato.autor