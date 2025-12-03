from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View 
from django.views.generic import ListView, CreateView, DetailView, TemplateView, DeleteView, UpdateView

from .forms import RelatoForm, ComentarioForm
from django.urls import reverse_lazy

from django.http import HttpResponse, HttpResponseRedirect


#importacion del modelo Relato y categoria
from .models import Relato, Categoria, Comentario

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comentario_form"] = ComentarioForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()   # Relato actual
        if "comentario_id" in request.POST:
            comentario = get_object_or_404(Comentario, id=request.POST["comentario_id"])

            if comentario.autor != request.user:
                return HttpResponse("No puedes editar este comentario.", status=403)

            comentario.contenido = request.POST.get("contenido_editado")
            comentario.save()

            return redirect("detalle_relato", pk=self.object.pk)

    
        form = ComentarioForm(request.POST)

        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.relato = self.object
            comentario.save()
            return redirect("detalle_relato", pk=self.object.pk)

        context = self.get_context_data()
        context["comentario_form"] = form
        return self.render_to_response(context)
    
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
    
    
class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        relato = Relato.objects.get(pk=pk)
        user = request.user

        # Si tiene dislike, se lo quitamos
        if relato.dislikes.filter(id=user.id).exists():
            relato.dislikes.remove(user)

        # Lógica de like: toggle
        if relato.likes.filter(id=user.id).exists():
            # Ya dio like, se remueve
            relato.likes.remove(user)
        else:
            # No hay like, se agrega
            relato.likes.add(user)

        # redireccion
        next_url = request.POST.get('next', '/')
        return HttpResponseRedirect(next_url)
        
            
class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        relato = Relato.objects.get(pk=pk)
        user = request.user

        # Si tiene like, se lo quitamos
        if relato.likes.filter(id=user.id).exists():
            relato.likes.remove(user)

        # Toggle de dislike
        if relato.dislikes.filter(id=user.id).exists():
            relato.dislikes.remove(user)
        else:
            relato.dislikes.add(user)

        next_url = request.POST.get('next', '/')
        return HttpResponseRedirect(next_url)
    
"""   
## para agregar categorias desde una vista
from django.http import HttpResponse
from .models import Categoria

def resetear_categorias(request):
    # 1. Eliminar todas las categorías
    Categoria.objects.all().delete()

    # 2. Crear nuevas categorías
    nuevas = ["Memoria Ancestral", "Historia Mapuche", "Identidad y Cultura", "Resistencia y Pueblo"]
    for nombre in nuevas:
        Categoria.objects.create(nombre=nombre)

    return HttpResponse("Categorías actualizadas correctamente.")

""" 