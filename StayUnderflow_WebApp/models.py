from django.db import models
from django import forms
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

from utils.time import get_time_local
from django.urls import reverse
from django.utils.safestring import mark_safe

# Classe que guardarà la informació de cada post
class Post(models.Model):
    title = models.CharField(max_length=100, help_text= mark_safe("Tips on posting a good question:<br>   - Make sure your question has not been asked already.<br>   - Keep your Title short and to the point.<br>   - Double-check grammar and spelling in both Title and Content of the post."))
    content = models.TextField()
    # documentació https://docs.djangoproject.com/en/2.2/ref/templates/builtins/#date
    date_posted = models.DateTimeField(default=get_time_local()) # en el cas de no posar data es posa la data actual del sistema per defecte
    author = models.ForeignKey(User, on_delete= models.CASCADE) # quan s'elimina un usuari també s'eliminen els seus posts

    tags = TaggableManager()

    def __str__(self):
        return self.title

    # retorna la direcció a el post després de crear-lo
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self,pk):
        return reverse('post-detail', kwargs={'pk': pk})


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

    best = models.fields.BooleanField(default=False)

    likes = models.ManyToManyField(Like)


    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'Perfil de {self.user.username}'

