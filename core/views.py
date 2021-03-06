from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import Http404
from django.urls import Resolver404
from .forms import SignupForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from lessons.models import Lesson
from datetime import timedelta, datetime

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
    minTime = now + timedelta(days=365)
    hasReviews = False
    for lesson in lessons:
        if lesson.next_review_time:
            hasReviews = True
            if lesson.next_review_time <= now:
                numReviews += 1
            elif lesson.next_review_time < minTime:
                minTime = lesson.next_review_time

    return render(
        request, 
        'profile.html', 
        {
            'lessons': lessons,
            'now': now,
            'numReviews': numReviews,
            'hasReviews': hasReviews,
            'nextReviewTime': minTime,
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
            # Return the form with its error messages to display to user
            return render(request, 'signup.html', {'form': form})
    else:
        return render(request, 'signup.html', {'form': SignupForm()})

def handler404(request, exception):
    return render(request, '404.html')
