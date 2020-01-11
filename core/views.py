from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'login.html')

def profile(request):
    if request.user is not None and request.user.is_authenticated:
        return render(request, 'profile.html')
    return redirect('login')