from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Classe que guardarà la informació de cada post
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # documentació https://docs.djangoproject.com/en/2.2/ref/templates/builtins/#date
    date_posted = models.DateTimeField(default=timezone.now) # en el cas de no posar data es posa la data actual del sistema per defecte
    author = models.ForeignKey(User, on_delete= models.CASCADE) # quan s'elimina un usuari també s'eliminen els seus posts

    def __str__(self):
        return self.title

    # retorna la direcció a el post després de crear-lo
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})