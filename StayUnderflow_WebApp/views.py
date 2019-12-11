from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from .models import Post, Answer, User, Like, Perfil
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
import operator

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
    posts = [(x.title,x.content, x.id, x.views) for x in Post.objects.filter(author_id=request.user.pk)]
    answers = [(x.post_id,x.content) for x in Answer.objects.filter(author_id=request.user.pk)]
    answers = [(y,Post.objects.get(id=x).title,x) for x,y in answers]

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

def search_bar(request):
    return search_tags(request) if request.GET.get("search_options") == 'tag_post' else search_users(request)


def search_users(request):
    username = request.GET.get("search_v", None)

    users_list = [x.username for x in User.objects.filter(username__icontains=username) if username != ""]

    return render(request, 'stay_underflow/users.html', {
            "user_list": users_list
        })

def search_tags(request):
    print(request.GET)
    return render(request, 'stay_underflow/stayunderflow.html', {
        "posts": Post.objects.filter(tags__name__in=[request.GET.get("search_v", None)])
    })

def other_profile(request,username=""):
    id = User.objects.get(username=username).id
    profile_user = User.objects.get(username=username)

    posts = [(x.title,x.content,x.id, x.views) for x in Post.objects.filter(author_id=id)]
    answers = [(x.post_id, x.content) for x in Answer.objects.filter(author_id=id)]
    answers = [(y, Post.objects.get(id=x).title,x) for x, y in answers]

    return render(request, 'stay_underflow/others_profile.html', {
        "profile_user":profile_user,
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
        an.author.perfil.reputation += 10

    else:
        an.likes.remove(likes[0])
        likes[0].delete()
        an.author.perfil.reputation -= 10
        if an.author.perfil.recompensa < 1: an.author.perfil.reputation = 1

    an.author.perfil.save()

    return redirect('/stayunderflow/post/' + str(pk) + '/')

@login_required()
def best_ans(request,pk,id):
    an = Answer.objects.get(id = id)
    post = Post.objects.get(id = pk)
    
    perfil = request.user.perfil

    if an.best:
        an.best = False
        an.author.perfil.reputation -= 20
        if an.author.perfil.recompensa < 1: an.author.perfil.reputation = 1
        perfil.reputation -= 2
        if perfil.reputation < 1: perfil.reputation = 1

    else:
        an.best = True
        post.done = True
        an.author.perfil.reputation += 20
        perfil.reputation += 2

    an.save()
    an.author.perfil.save()

    all_answers = Answer.objects.filter(post_id=pk).filter(best=True)
    if all_answers.__len__() == 0:
        post.done = False

    post.save()

    if not perfil.recompensa:
        perfil.reputation += 50
        perfil.recompensa = True

    perfil.save()

    return redirect('/stayunderflow/post/' + str(pk) + '/')


class Stayunderflow(ListView):
    model =  Post # classe que agafa per anar a buscar les dades
    template_name = 'stay_underflow/stayunderflow.html' #pagina web que utilitza per a carregar la view
    context_object_name = 'posts' # llista que utilitza (a la view) per ordenar
    ordering = ['-date_posted'] # ordena els posts de data més recent a menys

    def get_context_data(self, **kwargs):
        context = super(Stayunderflow,self).get_context_data(**kwargs)

        context['done'] = context['posts'].filter(done=True)
        context['undone'] = context['posts'].filter(done=False)

        
        llista = []
        hot = []
        for post in context['posts']:
            if len(post.answer_set.all()) == 0:
                llista.append(post)
            if post.views >= 100:
                hot.append(post)

        context['hot'] = hot
        context['unanswered'] = llista

        return context


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

        x = [(x,x.likes.count()) for x in context['post'].answer_set.all()]
        x.sort(key = lambda x:x[1], reverse = True)
        context['answers'] = [y[0] for y in x]

        post = Post.objects.get(id=context['post'].id)
        post.views = post.views+1
        post.save()

        context['views'] = post.views

        if post.views >= 10 and post.views < 25:
            context["medalla"] = 1
        elif post.views >= 25 and post.views < 100:
            context["medalla"] = 2
        elif post.views >= 100:
            context["medalla"] = 3
        else:
            context["medalla"] = 0

        context['referencia'] = context['post'].referencia_a

        if context['post'].referencia_a != -1:
            context['nom_referencia'] = Post.objects.get(pk=context['post'].referencia_a).title

        return context

class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'tags']
    template_name = 'stay_underflow/post_form.html'

    def form_valid(self, form):
        if 'pk' in self.kwargs:
            form.instance.referencia_a = self.kwargs['pk']

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
