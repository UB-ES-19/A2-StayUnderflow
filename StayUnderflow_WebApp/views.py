from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegisterForm
from django.contrib import messages
from .models import Post
from django.views.generic import DetailView

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

# Testejar si realment ens hem loguejat
def stayunderflow(request):
    if request.user.username == '':
        logged = False
        username = ''
    else:
        logged = True
        username = request.user.username
        context = { 'posts': Post.objects.all(), 'username':username, 'logged':logged}
        return render(request, 'stay_underflow/stayunderflow_postView.html', context)

    return render(request, 'stay_underflow/stayunderflow.html', {
        'username':username,
         'logged':logged
    })

class PostDetailView(DetailView):
    model = Post
    template_name = 'stay_underflow/post_detail.html'
