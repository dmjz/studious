from django.urls import path
from core.views import index, login, profile

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
]