from django.urls import path
from . import views
from .views import send_magic_link, verify_magic_link
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('send-magic-link/', send_magic_link, name='send_magic_link'),
    path('verify-magic-link/<str:uidb64>/<str:token>', verify_magic_link, name='verify_magic_link'),
    path('registration/', views.registration, name='registration'),
    path('base/', views.base, name='base'),
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentication/logout.html'), name='logout'),
]
