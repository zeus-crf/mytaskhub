from django.urls import path
from django.contrib.auth import views as auth_views # Views de autentificação 
from users import views as user_views


urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', user_views.logout_view, name='logout'),
    path('register', user_views.register, name='register'),
]
