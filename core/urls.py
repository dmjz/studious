from django.urls import path
from django.contrib.auth import views as auth_views
from core.views import home, logout_view, profile, password_done, signup

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login',
    ),
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change',
    ),
    path(
        'password-change/done/', 
        password_done,
        name='password_change_done',
    ),
]