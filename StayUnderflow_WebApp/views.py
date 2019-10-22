from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from .models import Post, Answer, User, Like
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
    return render(request, 'stay_underflow/stayunderflow_home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(form.as_p())
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, f'Account succesfuly created for {username}!')
            user = auth.authenticate(username=username,password=password)
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile')
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

@login_required()
def update_my_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        image_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.perfil)
        if user_form.is_valid() and image_form.is_valid():
            user_form.save()
            image_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        image_form = ProfileUpdateForm(instance=request.user.perfil)

    context = {'user_form': user_form, 'image_form': image_form}

    return render(request, 'stay_underflow/edit_profile.html', context)

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

@login_required()
def like_ans(request,pk,id):
    an = Answer.objects.get(id = id)
    likes = an.likes.filter(author = request.user.id)

    if likes.__len__() == 0:
        l = Like(author=User.objects.get(id=request.user.id))
        l.save()
        an.likes.add(l)
    else:
        an.likes.remove(likes[0])
        likes[0].delete()

    return redirect('/stayunderflow/post/' + str(pk) + '/')

@login_required()
def best_ans(request,pk,id):
    an = Answer.objects.get(id = id)

    if an.best:
        an.best = False
    else:
        an.best = True
    an.save()

    return redirect('/stayunderflow/post/' + str(pk) + '/')


class Stayunderflow(ListView):
    model =  Post # classe que agafa per anar a buscar les dades
    template_name = 'stay_underflow/stayunderflow.html' #pagina web que utilitza per a carregar la view
    context_object_name = 'posts' # llista que utilitza (a la view) per ordenar
    ordering = ['-date_posted'] # ordena els posts de data més recent a menys

class PostsByTag(ListView):
    template_name = 'stay_underflow/stayunderflow.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags__name__in=[self.kwargs['tag']])

class PostDetailView(DetailView):
    model = Post
    template_name = 'stay_underflow/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView,self).get_context_data(**kwargs)
        context['owner'] = self.request.user.id == context['post'].author_id
        return context

class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'tags']
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
