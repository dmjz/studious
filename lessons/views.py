from django.shortcuts import render, redirect
from lessons.lessons import lesson_from_post, save_lesson
from lessons.models import Lesson
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import json

def new(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        # Create and save new lesson
        lessonData = json.dumps(lesson_from_post(request.POST))
        lesson = Lesson(
            owner   = request.user,
            created = timezone.now(), 
            file    = ContentFile(lessonData, name='dummy_name'),
        )
        lesson.save()
        return redirect('profile')
    return render(request, 'new.html')

def edit(request):
    return render(request, 'edit.html')

def view(request):
    return render(request, 'view.html')


def test_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        print(myfile)
        print(type(myfile))
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'test_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'test_upload.html')