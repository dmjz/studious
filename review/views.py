from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from lessons.models import Lesson

def round_hour(dt):
    """ Round datetime to nearest hour """
    if dt.minute >= 30: 
        return dt.replace(hour=dt.hour+1, minute=0, second=0, microsecond=0)
    return dt.replace(minute=0, second=0, microsecond=0)

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def review(request):
    return render(request, 'review.html', {})

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def add_review(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.user == lesson.owner:
        lesson.review_started = timezone.now()
        lesson.next_review_time = timezone.now()
        lesson.save(update_fields=['review_started', 'next_review_time'])
    return redirect('profile') 