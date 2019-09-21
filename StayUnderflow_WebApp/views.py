from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = UserCreationForm()
    return render(request, 'stay_underflow/register.html', {
        'form': form,
    })