from django.urls import path
from . import views
from .views import *

urlpatterns = [    
    path('home/', HomeView.as_view(), name='home'), 
    path('no_permiso/', NoPermiso.as_view(), name='no_permiso'),
    path('registro_exitoso/', RegistroExitoso.as_view(), name='registro_exitoso'), 
    path('relatos', ListaRelatosView.as_view(), name='relatos'),
    path('relato/nuevo/', RelatoCreateView.as_view(), name='nuevo_relato'),
    path('relato/<int:pk>/', RelatoDetailView.as_view(), name='detalle_relato'),
    path('relato/<int:pk>/editar/', RelatoUpdateView.as_view(), name='editar_relato'),
    path('relato/<int:pk>/eliminar/', RelatoDeleteView.as_view(), name='eliminar_relato'),
    path("relato/<int:pk>/", RelatoDetailView.as_view(), name="detalle_relato"),
    
    path('like/<int:pk>/', AddLike.as_view(), name='add_like'),
    path('dislike/<int:pk>/', AddDislike.as_view(), name='add_dislike'),
    
]