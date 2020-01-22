from django.shortcuts import render, redirect, get_object_or_404
from lessons.models import Lesson
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import json
from django.contrib.auth.decorators import login_required
from django.http import Http404

def get_validated_lesson_data(request):
    """ From a request, raise Http404 or return validated lessonData """

    lessonData = {
        'title':    request.POST.get('titleFormInput'),
        'lesson':   request.POST.get('fullLessonFormTextarea'),
        'examples': request.POST.get('examplesFormTextarea'),
    }
    for field, maxLength in (('title', 500), ('lesson', 10000), ('examples', 2000)):
        if not lessonData.get(field):
            raise Http404(f'The required lesson field { field } is missing or empty.')
        if len(lessonData[field]) > maxLength:
            raise Http404(f'Sorry, the { field } section is too long! The max length is { maxLength } characters.')
    return lessonData

def read_lesson_data(lesson):
    lesson.file.open(mode='r')
    lessonData = json.loads(lesson.file.read())
    lesson.file.close()
    return lessonData

@login_required
def new(request):
    if request.method == 'POST':
        # Create and save new lesson
        lessonData = get_validated_lesson_data(request)
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
            return redirect('profile')
        if not lesson:
            raise Http404('For an unknown reason, we failed to save the lesson. Sorry!')
    else:
        return render(request, 'new.html')

@login_required
def edit(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.user != lesson.owner:
        return redirect('view', lesson_id=lesson_id)
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
        return render(
            request, 
            'edit.html', 
            {'lesson': lessonData, 'lesson_id': lesson_id},
        )

@login_required
def view(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    lessonData = read_lesson_data(lesson)
    return render(
        request, 
        'view.html', 
        {'lesson': lessonData, 'lesson_id': lesson_id},
    )