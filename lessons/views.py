from django.shortcuts import render, redirect
from lessons.lessons import lesson_from_post, save_lesson
from lessons.models import Lesson
from datetime import datetime

def new(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        # Create and save new lesson
        lessonData = lesson_from_post(request.POST)
        lessonObject = Lesson(owner=request.user, created=datetime.now())
        lessonObject.save()
        lessonData['id'] = lessonObject.uuid
        save_lesson(request.user, lessonData)
        return redirect('profile')
    return render(request, 'new.html')

def edit(request):
    return render(request, 'edit.html')

def view(request):
    return render(request, 'view.html')