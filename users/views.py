from lib2to3.fixes.fix_input import context

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserCreationForm, UserLoginForm, EditProfileForm


class Profile(View, LoginRequiredMixin):
    def get(self, request):
        context = {
            "user": request.user
        }
        return render(request, 'users/profile.html', context)


class EditProfile(View, LoginRequiredMixin):
    def get(self, request):
        user_form = EditProfileForm(instance=request.user)
        context = {
            "form": user_form
        }
        return render(request, 'users/edit.html', context)

    def post(self, request):
        user_form = EditProfileForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user
        )
        if user_form.is_valid():
            user_form.save()
            return redirect('users:profile')
        context = {
            "form": user_form
        }
        return render(request, 'users/edit.html', context)


class LogoutView(View, LoginRequiredMixin):
    def get(self, request):
        logout(request)
        return redirect('users:login')


class LoginView(View):
    def get(self, request):
        user_form = UserLoginForm()
        context = {
            "form": user_form
        }
        return render(request, 'users/login.html', context)

    def post(self, request):
        login_form = UserLoginForm(data=request.POST)
        context = {
            "form": login_form
        }
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('common:home')
        return render(request, 'users/login.html', context)


class RegisterView(View):
    def get(self, request):
        create_form = UserCreationForm()
        context = {
            'form': create_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        create_form = UserCreationForm(data=request.POST, files=request.FILES)
        context = {
            'form': create_form
        }
        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        return render(request, 'users/register.html', context)
