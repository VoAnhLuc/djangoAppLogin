from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms_auth import UsersCreationFrom, UsersLoginFrom

# Create your views here.

def login(request):
    form = UsersLoginFrom()
    if request.method == 'POST':
        form = UsersLoginFrom(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            is_auth = authenticate(request, email=email, password=password)
            if is_auth is not None:
                auth_login(request, is_auth),
                return redirect('users:dashboard')
            else:
                messages.warning(request, 'Email or Password is not incorrect')

    context = {'form': form}
    return render(request, 'login/login.html', context)
def register(request):
    form = UsersCreationFrom()
    if request.method == 'POST':
        form = UsersCreationFrom(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account was created for ' + email)
            return redirect('users:dashboard')
    context = {'form': form}
    return render(request, 'login/register.html', context)

def dashboard(request):
    if request.user.is_authenticated:
        context = {
            'email': request.user,
        }
    else:
        context = {
            'email': 'not authentication',
        }
    return render(request, 'login/dashboard.html', context)

def logout_user(request):
    logout(request)
    return redirect('users:dashboard')
