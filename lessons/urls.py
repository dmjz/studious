from django.urls import path
from lessons.views import edit

urlpatterns = [
    path('edit', edit, name='edit'),
]