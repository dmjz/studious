from django.urls import path
from lessons.views import new, edit, view, publish, search, copy

urlpatterns = [
    path('new', new, name='new'),
    path('edit/<int:lesson_id>', edit, name='edit'),
    path('view/<int:lesson_id>', view, name='view'),
    path('publish/<int:lesson_id>', publish, name='publish'),
    path('search', search, name='search'),
    path('copy/<int:lesson_id>', copy, name='copy'),
]