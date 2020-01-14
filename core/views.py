from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import Http404
from django.urls import Resolver404
from .forms import SignupForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def password_change(request):
    return render(request, 'password_change.html')

def password_done(request):
    return redirect('profile')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1') # 'password' gets hash; 'password1' gets actual
            checkUser = authenticate(username=username, password=password)
            login(request, checkUser)
            return redirect('profile')
        else:
            message = '\n'.join((f'{k}: {v}' for k, v in form.errors.as_data().items()))
            raise Http404(message)
    else:
        return render(request, 'signup.html', {'form': SignupForm()})

def handler404(request, exception):
    return render(request, '404.html')
