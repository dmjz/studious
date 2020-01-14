from django.urls import path
from lessons.views import new, edit, view, test_upload

urlpatterns = [
    path('new', new, name='new'),
    path('edit', edit, name='edit'),
    path('view', view, name='view'),
    path('test_upload', test_upload, name='test_upload'),
]