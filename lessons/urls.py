from django.urls import path
from lessons.views import new, edit, view

urlpatterns = [
    path('new', new, name='new'),
    path('edit/<int:lesson_id>', edit, name='edit'),
    path('view/<int:lesson_id>', view, name='view'),
]