from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import PermissionDenied
from lessons.models import Lesson
import json
import string
import random
from lessons.utils import \
    get_new_lesson_data, get_validated_lesson_data, read_lesson_data, \
    csv_tags_to_hash_list, search_lessons

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def new(request):
    lessonData = get_validated_lesson_data(get_new_lesson_data());
    lesson = Lesson(
        owner   = request.user,
        title   = lessonData['title'],
        created = timezone.now(), 
        file    = ContentFile(
            json.dumps(lessonData).encode('utf-8'), 
            name='dummy_name'
        ),
    )
    if lesson:
        lesson.save()
        return redirect('edit', lesson_id=lesson.id)
    if not lesson:
        raise Http404('For an unknown reason, we failed to save the lesson. Sorry!')

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def edit(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.user != lesson.owner:
        raise PermissionDenied
    if request.method == 'POST':
        # Modify and save lesson
        lessonData = get_validated_lesson_data(request)
        lessonFile = ContentFile(
            json.dumps(lessonData).encode('utf-8'),
            name='dummy_name'
        )
        lesson.title, lesson.file = lessonData['title'], lessonFile
        lesson.save(update_fields=['title', 'file'])
        return redirect('view', lesson_id=lesson_id)
    else:
        lessonData = read_lesson_data(lesson)
        # Ensure at least 5 review q/a's for the template to show
        numShort = 5 - len(lessonData['examples'])
        if numShort > 0:
            lessonData['examples'] += [{'question': '', 'answer': ''}] * numShort
        return render(
            request, 
            'edit.html', 
            {
                'lesson': lessonData, 
                'lesson_id': lesson_id,
            },
        )

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def view(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.user != lesson.owner and not lesson.is_public:
        raise PermissionDenied
    lessonData = read_lesson_data(lesson)
    # Process the tags into hash list for display
    hashTags = csv_tags_to_hash_list(lessonData['tags'])
    return render(
        request, 
        'view.html', 
        {
            'lesson': lessonData, 
            'lesson_id': lesson_id, 
            'hashTags': hashTags,
        },
    )

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def publish(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.user != lesson.owner:
        return redirect('view', lesson_id=lesson_id)
    lesson.is_public = True
    lesson.save(update_fields=['is_public'])
    return redirect('profile')

def search(request):
    if request.method == 'POST':
        searchText = request.POST.get('search-input')
        terms, results = search_lessons(searchText)
        return render(request, 'search.html', { 'terms': terms, 'results': results })