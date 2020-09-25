from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth import authenticate, login

def home_view(request):
    user = request.user
    hello = 'Hello world'

    context = {
        'user': user,
        'hello' : hello,
    }
    return render(request, 'main/home.html', context)
    # return HttpResponse('Hello world')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)   # UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            valid_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, valid_user)
            return HttpResponseRedirect("/posts/")
    else:
        form = RegisterForm()  # UserCreationForm()

    return render(request, "register/register.html", {"form": form})
