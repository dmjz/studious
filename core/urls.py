from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from core.views import home, login, profile

urlpatterns = [
    path('', home, name='home'),
    path(
        'login/',
        LoginView.as_view(template_name='login.html'),
        name='login',
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name='logout.html'),
        name='logout',
    ),
    path('profile/', profile, name='profile'),
]