from django.db import models
from django import forms
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

from stay_underflow.constants import Flags
from utils.time import get_time_local
from django.urls import reverse
from django.utils.safestring import mark_safe


# Classe que guardarà la informació de cada post
class Post(models.Model):
    title = models.CharField(max_length=100, help_text= mark_safe("Tips on posting a good question:<br>   - Make sure your question has not been asked already.<br>   - Keep your Title short and to the point.<br>   - Double-check grammar and spelling in both Title and Content of the post."))
    content = models.TextField()
    # documentació https://docs.djangoproject.com/en/2.2/ref/templates/builtins/#date
    date_posted = models.DateTimeField(default=get_time_local())  # en el cas de no posar data es posa la data actual del sistema per defecte
    author = models.ForeignKey(User, on_delete= models.CASCADE)  # quan s'elimina un usuari també s'eliminen els seus posts

    done = models.fields.BooleanField(default=False)
    referencia_a = models.IntegerField(default=-1)

    image = models.ImageField(default='default', upload_to='post_pics')

    tags = TaggableManager()
    hidden = models.BooleanField(default=False)

    views = models.IntegerField(default=0)

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

    image = models.ImageField(default='default', upload_to='answer_pics')

    # Per defecte, la data del sistema
    date_posted = models.DateTimeField(default=get_time_local())

    best = models.fields.BooleanField(default=False)

    hidden = models.BooleanField(default=False)

    # L'autor de la resposta
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # El post al qual responem
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    likes = models.ManyToManyField(Like)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    reputation = models.IntegerField(default=1)
    recompensa = models.BooleanField(default=False)

    def __str__(self):
        return f'Perfil de {self.user.username}'


class FlagPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    descripcion = models.CharField(
        max_length=100,
        choices=[(tag.value, tag.name) for tag in Flags]
    )

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})


class FlagAnswer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    descripcion = models.CharField(
        max_length=100,
        choices=[(tag.value, tag.name) for tag in Flags]
    )

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.answer.post.pk})


class Favorite(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
