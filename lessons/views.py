from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.http import Http404
from lessons.models import Lesson
import json
import string
import random

def random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def get_new_lesson_data():
    """ Return an empty lesson (for new lesson creation) """

    return  {
        'title':    f'New lesson (#{ random_string(8) })',
        'lesson':   '',
        'examples': [],
    }

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
                examples.append({'question': question, 'answer': answer})
                
    lessonData = {
        'title':    request.POST.get('titleFormInput'),
        'lesson':   request.POST.get('fullLessonFormTextarea'),
        'examples': examples,
    }
    
    for field, maxLength in (('title', 500), ('lesson', 10000), ('examples', 500)):
        if lessonData.get(field) is None:
            raise Http404(f'The required lesson field "{ field }" is missing')
        if field == 'examples':
            examples = lessonData[field]
            for i, ex in enumerate(examples):
                if len(ex['question']) > maxLength or len(ex['answer']) > maxLength:
                    raise Http404(f'Sorry, review question { i } is too long. The max length is { maxLength } characters.')        
        elif len(lessonData[field]) > maxLength:
            raise Http404(f'Sorry, the { field } section is too long. The max length is { maxLength } characters.')
    return lessonData

def read_lesson_data(lesson):
    lesson.file.open(mode='r')
    lessonData = json.loads(lesson.file.read())
    lesson.file.close()
    return lessonData

@login_required(login_url=settings.LOGIN_REQUIRED_REDIRECT)
def new(request):
    lessonData = get_new_lesson_data();
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
        # Ensure at least 5 review q/a's for the template to show
        numShort = 5 - len(lessonData['examples'])
        if numShort > 0:
            lessonData['examples'] += [{'question': '', 'answer': ''}] * numShort
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