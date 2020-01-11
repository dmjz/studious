from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import Http404
from .forms import SignupForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

# TODO: use a decorator to actually implement this
# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('profile')
#     return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    return redirect('login')

def password_change(request):
    if request.user.is_authenticated:
        return render(request, 'password_change.html')
    return redirect('login')

def password_done(request):
    return redirect('profile')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is None:
                raise Http404(
                    'Sorry, we couldn\'t sign you up. Maybe the username or email is already registered?'
                )
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1') # 'password' gets hash; 'password1' gets actual
            checkUser = authenticate(username=username, password=password)
            if checkUser is None:
                raise Http404(
                    'Sorry, something went wrong when we tried to log you in.'
                    '\nTry logging in manually. If this doesn\'t work, you may need to create a new account.'
                )
            login(request, checkUser)
            return redirect('profile')
        else:
            raise Http404(str(form.errors.as_data()))
    else:
        return render(request, 'signup.html', {'form': SignupForm()})
