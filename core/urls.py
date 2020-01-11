from django.urls import path
from core.views import home, login, profile

urlpatterns = [
    path('', index, name='home'),
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
]