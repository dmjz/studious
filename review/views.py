from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from lessons.models import Lesson
from lessons.utils import get_review_QnAs

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

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def available(request):
    print('Available called')
    lessons = Lesson.objects.filter(owner=request.user.id)
    now = timezone.now()
    return JsonResponse({
        'reviews': [
            {
                'lesson_id': lesson.id,
                'qna_pairs': get_review_QnAs(lesson),
            }
            for lesson in lessons
            if lesson.next_review_time and lesson.next_review_time <= now
        ]
    })