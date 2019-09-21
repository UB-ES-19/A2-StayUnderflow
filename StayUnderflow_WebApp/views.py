from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form.as_p())
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = UserCreationForm()
    return render(request, 'stay_underflow/register.html', {
        'form': form,
    })

def login_m(request):
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
                return HttpResponseRedirect(reverse("test_login"))
    else:
        connection_form = AuthenticationForm()
    return render(request, 'stay_underflow/login.html', {'form' : connection_form})

# Testejar si realment ens hem loguejat
@login_required(login_url='/login/')
def test_login(request):
    return HttpResponse("Podem arribar aqui")