from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import Http404
from django.urls import Resolver404
from .forms import SignupForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from lessons.models import Lesson

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def profile(request):
    lessons = Lesson.objects.filter(owner=request.user.id)
    now = timezone.now()
    numReviews = 0
    for lesson in lessons:
        if lesson.next_review_time and lesson.next_review_time <= now:
            numReviews += 1
    return render(
        request, 
        'profile.html', 
        {
            'lessons': lessons,
            'now': now,
            'numReviews': numReviews,
        },
    )

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
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
