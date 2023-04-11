from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms_auth import UsersCreationFrom, UsersLoginFrom
from django.views import View

# Create your views here.

class Login(View):
    form_class = UsersLoginFrom
    template_name = 'login/login.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            is_auth = authenticate(request, email=email, password=password)

            if is_auth is not None:
                auth_login(request, is_auth),
                return redirect('users:dashboard')
            else:
                messages.warning(request, 'Email or Password is not incorrect')

        return render(request, self.template_name, {'form': form})
class Register(View):
    form_class = UsersCreationFrom
    template_name = 'login/register.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})
    def post(self, request, *args, **kwargs):
        # form = UsersCreationFrom()
        # if request.method == 'POST':
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account was created for ' + email)
            return redirect('users:dashboard')

        return render(request, 'login/register.html', {'form': form})

class Dashboard(View):
    template_name = 'login/dashboard.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = request.user.get_info()
        else:
            context = {
                'email': 'not authentication',
            }
        return render(request, self.template_name, context)

class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('users:dashboard')
