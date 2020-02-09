from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from datetime import timedelta
from lessons.models import Lesson
from lessons.utils import get_review_QnAs, update_review_fields
import json

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

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def save_progress(request):
    if request.method != 'POST':
        return redirect('profile')
    if not request.POST.get('reviews'):
        raise KeyError('Expected "reviews" in POST data')
    reviews = json.loads(request.POST.get('reviews'))
    for review in reviews:
        lesson = get_object_or_404(Lesson, pk=review['lesson_id'])
        if lesson.owner != request.user:
            raise PermissionDenied('You don\'t have permission to modify this lesson\'s review status.')
        if review['is_done']:
            if review['was_ever_incorrect']:
                update_review_fields(lesson, isCorrect=False)
            else: 
                update_review_fields(lesson, isCorrect=True)
    return JsonResponse({
        'status': 200, 
        'statusText': 'OK',
        'redirect': reverse('profile'),
    })