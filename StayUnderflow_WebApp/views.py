from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegisterForm
from django.contrib import messages
from .models import Post, Answer
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

# métode login gestionat amb django
""""def login_m(request):
    if request.method == 'POST':
        connection_form = AuthenticationForm(data=request.POST)
        print(connection_form.as_p())
        if connection_form.is_valid():
            print("B")
            username = connection_form.cleaned_data["username"]
            password = connection_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("A")
                return HttpResponseRedirect(reverse("stayunderflow"))
    else:
        connection_form = AuthenticationForm()
    return render(request, 'stay_underflow/login.html', {'form' : connection_form})"""
