from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.contrib.auth.models import User
from lessons.models import Lesson
import json
import string
import random
from lessons.utils import \
    get_new_lesson_data, get_validated_lesson_data, read_lesson_data, \
    search_lessons, hash_tags

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def new(request):
    """ Create a new lesson from scratch """

    lessonData = get_validated_lesson_data(get_new_lesson_data());
    lesson = Lesson(
        owner   = request.user,
        title   = lessonData['title'],
        tags    = lessonData['tags'],
        created = timezone.now(), 
        file    = ContentFile(
            json.dumps(lessonData).encode('utf-8'), 
            name='dummy_name'
        ),
        original_owner = request.user,
        original_lesson = None,
    )
    if lesson:
        lesson.save()
        return redirect('edit', lesson_id=lesson.id)
    if not lesson:
        raise Http404('For an unknown reason, we failed to save the lesson. Sorry!')

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def edit(request, lesson_id):
    """ Save edits to a lesson (if POST) or render lesson edit page """

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
        lesson.title, lesson.file, lesson.tags = lessonData['title'], lessonFile, lessonData['tags']
        lesson.save(update_fields=['title', 'file', 'tags'])
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
    """ Render the lesson view page """

    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.user != lesson.owner and not lesson.is_public:
        raise PermissionDenied
    originalLessonId = str(lesson.original_lesson.id) if lesson.original_lesson else 'None'
    originalOwnerName = lesson.original_owner.username if lesson.original_owner else ''
    lessonData = read_lesson_data(lesson)
    hashTags = hash_tags(lessonData.get('tags'))
    isOwned = (request.user == lesson.owner)
    return render(
        request, 
        'view.html', 
        {
            'lesson': lessonData, 
            'lesson_id': lesson_id,
            'hash_tags': hashTags,
            'is_owned': isOwned,
            'original_lesson_id': originalLessonId,
            'original_owner': originalOwnerName,
        },
    )

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def publish(request, lesson_id):
    """ Publish the lesson (becomes searchable and viewable to non-owners) """

    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.user != lesson.owner:
        return redirect('view', lesson_id=lesson_id)
    lesson.is_public = True
    lesson.save(update_fields=['is_public'])
    return redirect('profile')

def search(request):
    """ Search public lessons using POSTed search text """

    if request.method == 'POST':
        searchText = request.POST.get('search-input')
        terms, results = search_lessons(searchText)
        return render(
            request, 
            'search.html', 
            { 
                'terms': terms, 
                'results': [
                    {'lesson': lesson, 'hash_tags': hash_tags(lesson.tags)}
                    for lesson in results
                ]
            }
        )

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def copy(request, lesson_id):
    """ Create a user-owned copy of the lesson """

    lessonOriginal = get_object_or_404(Lesson, pk=lesson_id)
    dataOriginal = read_lesson_data(lessonOriginal)
    ownerOriginal = lessonOriginal.owner
    lessonCopy = Lesson(
        owner   = request.user,
        title   = dataOriginal['title'],
        tags    = dataOriginal['tags'],
        created = timezone.now(), 
        file    = ContentFile(
            json.dumps(dataOriginal).encode('utf-8'), 
            name='dummy_name'
        ),
        original_owner = lessonOriginal.owner,
        original_lesson = lessonOriginal,
    )
    if lessonCopy:
        lessonCopy.save()
        lessonOriginal.times_copied = F('times_copied') + 1
        lessonOriginal.save(update_fields=['times_copied'])
        return redirect('edit', lesson_id=lessonCopy.id)
    if not lessonCopy:
        raise Http404('For an unknown reason, we failed to copy the lesson. Sorry!')

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def delete(request):
    """ Delete lesson (lesson_id submitted in form) """

    if request.method != 'POST':
        return redirect('profile')
    lesson_id = request.POST.get('delete-lesson-id')
    if not lesson_id:
        return redirect('profile')
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.user != lesson.owner:
        raise PermissionDenied
    else:
        print(f'Delete lesson { lesson_id }')
        lesson.delete()
        return redirect('profile')