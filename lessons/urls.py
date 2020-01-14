from django.urls import path
from lessons.views import new, edit, view

urlpatterns = [
    path('new', new, name='new'),
    path('edit', edit, name='edit'),
    path('view/<int:user_id>/<int:lesson_id>', view, name='view'),
]