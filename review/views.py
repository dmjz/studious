from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils import timezone
from django.conf import settings
from lessons.models import Lesson

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def review(request):
    return render(request, 'review.html', {}) 