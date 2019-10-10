from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegisterForm
from django.contrib import messages
from .models import Post, Answer, User
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(form.as_p())
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account succesfuly created for {username}!')
            return redirect('stayunderflow')
    else:
        form = UserRegisterForm()
    return render(request, 'stay_underflow/register.html', {
        'form': form,
    })

@login_required()
def my_profile(request):
    posts = [(x.title,x.content) for x in Post.objects.filter(author_id=request.user.pk)]
    answers = [(x.post_id,x.content) for x in Answer.objects.filter(author_id=request.user.pk)]
    answers = [(y,Post.objects.get(id=x).title) for x,y in answers]

    return render(request, 'stay_underflow/profile.html', {
        "username":request.user.username,
        "posts": posts,
        "answers" : answers
    })

def search_users(request):
    username = request.GET["username"]

    users_list = [x.username for x in User.objects.filter(username__icontains=username) if username != ""]

    return render(request, 'stay_underflow/users.html', {
            "user_list": users_list
        })

def other_profile(request,username=""):
    id = User.objects.get(username=username).id

    posts = [(x.title,x.content) for x in Post.objects.filter(author_id=id)]
    answers = [(x.post_id, x.content) for x in Answer.objects.filter(author_id=id)]
    answers = [(y, Post.objects.get(id=x).title) for x, y in answers]

    return render(request, 'stay_underflow/profile.html', {
        "username":username,
        "posts": posts,
        "answers": answers
    })

class Stayunderflow(ListView):
    model =  Post # classe que agafa per anar a buscar les dades
    template_name = 'stay_underflow/stayunderflow.html' #pagina web que utilitza per a carregar la view
    context_object_name = 'posts' # llista que utilitza (a la view) per ordenar
    ordering = ['-date_posted'] # ordena els posts de data més recent a menys

class PostDetailView(DetailView):
    model = Post
    template_name = 'stay_underflow/post_detail.html'

class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'stay_underflow/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CreateAnswer(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['content']
    template_name = 'stay_underflow/answer_form.html'

    def form_valid(self, form):
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)
