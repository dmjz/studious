from django.urls import path
from lessons.views import new, edit, view

urlpatterns = [
    path('new', new, name='new'),
    path('edit', edit, name='edit'),
    path('view', view, name='view'),
]