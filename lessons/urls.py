from django.urls import path
from lessons.views import index, edit

urlpatterns = [
    path('', index, name='index'),
    path('edit', edit, name='edit'),
]