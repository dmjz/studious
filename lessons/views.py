from django.shortcuts import render, redirect
from lessons.models import Lesson
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import json
from django.contrib.auth.decorators import login_required

@login_required
def new(request):
    if request.method == 'POST':
        # Create and save new lesson
        lessonData = {
            'title':    request.POST.get('titleFormInput'),
            'lesson':   request.POST.get('fullLessonFormTextarea'),
            'examples': request.POST.get('examplesFormTextarea'),
        }
        lessonData = json.dumps(lessonData)
        lesson = Lesson(
            owner   = request.user,
            created = timezone.now(), 
            file    = ContentFile(lessonData, name='dummy_name'),
        )
        lesson.save()
        return redirect('profile')
    return render(request, 'new.html')

@login_required
def edit(request):
    return render(request, 'edit.html')

@login_required
def view(request, user_id, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    lesson.file.open(mode='r')
    lessonData = json.loads(lesson.file.read())
    lesson.file.close()
    return render(request, 'view.html', {'lesson': lessonData})