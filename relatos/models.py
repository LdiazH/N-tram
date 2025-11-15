from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre
    
    
class Relato(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    
    def save(self, *args, **kwargs):
        # titulo en mayusculas
        if self.titulo:
            self.titulo = self.titulo.strip().capitalize()
        if self.contenido:
        #contenido en mayusculas
            self.contenido = self.contenido.strip().capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
    
    
class Comentario(models.Model):
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    relato = models.ForeignKey(Relato, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
        ordering = ['-fecha'] #Por defecto siempre me va a ordenar los más recientes primero

    def __str__(self):
        return self.contenido