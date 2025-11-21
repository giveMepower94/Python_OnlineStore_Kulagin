from django.urls import path
from .views import RegisterView, profile
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
