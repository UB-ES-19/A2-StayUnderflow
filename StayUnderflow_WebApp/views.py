from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegisterForm
from django.contrib import messages
from .models import Post, User#,Answer
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
    return render(request, 'stay_underflow/profile.html', {
        "posts": Post.objects.filter(author_id=request.user.pk),
        #"answers" : Answer.objects.filter(author_id=request.user.pk)
    })

def search_users(request,username=""):
    users_list = [x.username for x in User.objects.filter(username__icontains=username)]


    return render(request, 'stay_underflow/users.html', {
            "user_list": users_list
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