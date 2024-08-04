from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.utils import timezone
from .models import Profile
import pdb

User = get_user_model()

def send_magic_link(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        profile = Profile.objects.get_or_create(user=user)
        if user:
            token = get_random_string(32)
            user.profile.magic_token = token
            user.profile.token_created_at = timezone.now()
            user.profile.save()

            current_site = get_current_site(request)
            mail_subject = 'Your magic login link'
            # breakpoint()
            message = render_to_string('authentication/magic_link_email.html', {
                'user': user.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            send_mail(mail_subject, message, 'no-reply@example.com', [email])
            return HttpResponse('A magic link has been sent to your email.')
    return render(request, 'authentication/send_magic_link.html')

def verify_magic_link(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and user.profile.magic_token == token and not user.profile.is_token_expired():
        user.profile.magic_token = None
        user.profile.save()
        login(request, user)
        # breakpoint()
        request.session.set_expiry(10)
        return redirect('home')
    else:
        return HttpResponse('Invalid or expired link')

