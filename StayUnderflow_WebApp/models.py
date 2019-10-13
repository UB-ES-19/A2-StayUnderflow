from django.db import models
from django import forms
from django.contrib.auth.models import User
from utils.time import get_time_local
from django.urls import reverse

class Tag(models.Model):

    # Nom del tag
    name = models.TextField()

    def __str__(self):
        return self.name

# Classe que guardarà la informació de cada post
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # documentació https://docs.djangoproject.com/en/2.2/ref/templates/builtins/#date
    date_posted = models.DateTimeField(default=get_time_local()) # en el cas de no posar data es posa la data actual del sistema per defecte
    author = models.ForeignKey(User, on_delete= models.CASCADE) # quan s'elimina un usuari també s'eliminen els seus posts

    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    # retorna la direcció a el post després de crear-lo
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


# Classe per a guardar la informació de cada resposta
class Answer(models.Model):

    # Contingut de la resposta
    content = models.TextField()
    # Per defecte, la data del sistema
    date_posted = models.DateTimeField(default=get_time_local())
    # L'autor de la resposta
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # El post al qual responem
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})