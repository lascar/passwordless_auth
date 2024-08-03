from django.urls import path
from .views import send_magic_link, verify_magic_link

urlpatterns = [
    path('send-magic-link/', send_magic_link, name='send_magic_link'),
    path('verify-magic-link/<str:uidb64>/<str:token>', verify_magic_link, name='verify_magic_link'),
]
