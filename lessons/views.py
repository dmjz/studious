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

    examples = []
    for k, v in request.POST.items():
        # Only use non-empty questions and answers
        if 'question' in k and v:
            qid = k.split('-')[-1]
            question = v
            answer = request.POST.get(f'answer-{ qid }')
            if answer:
                examples.append((question, answer))
                
    lessonData = {
        'title':    request.POST.get('titleFormInput'),
        'lesson':   request.POST.get('fullLessonFormTextarea'),
        'examples': examples,
    }
    
    for field, maxLength in (('title', 500), ('lesson', 10000), ('examples', 500)):
        if not lessonData.get(field):
            raise Http404(f'The required lesson field { field } is missing or empty.')
        if field == 'examples':
            examples = lessonData[field]
            for i, (q, a) in enumerate(examples):
                if len(q) > maxLength or len(a) > maxLength:
                    raise Http404(f'Sorry, review question { i } is too long. The max length is { maxLength } characters.')        
        elif len(lessonData[field]) > maxLength:
            raise Http404(f'Sorry, the { field } section is too long! The max length is { maxLength } characters.')
    return lessonData

def read_lesson_data(lesson):
    lesson.file.open(mode='r')
    lessonData = json.loads(lesson.file.read())
    lesson.file.close()
    return lessonData

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
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

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
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

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def view(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    lessonData = read_lesson_data(lesson)
    return render(
        request, 
        'view.html', 
        {'lesson': lessonData, 'lesson_id': lesson_id},
    )