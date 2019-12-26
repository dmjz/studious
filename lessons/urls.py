from django.urls import path
from lessons.views import index

urlpatterns = [
    path('', index, name='index'),
]