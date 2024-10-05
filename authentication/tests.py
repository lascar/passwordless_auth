from django.test import TestCase
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.crypto import get_random_string
from django.test.client import RequestFactory
from unittest.mock import patch
from django.test import Client
from django.contrib.sessions.backends import db
from authentication.models import CustomUser
from .models import Profile
import pdb

TEST_NAME = 'Testuser'
TEST_EMAIL = 'toto@example.com'

class Expiry(TestCase):

    @classmethod
    def setUpClass(cls):
        super(Expiry, cls).setUpClass()
        cls.user = CustomUser.objects.create(username=TEST_NAME, email=TEST_EMAIL)
        cls.factory = RequestFactory()

    def test_authentication_by_magik_link_expire_in_10mn(self):
        profile = Profile.objects.get_or_create(user=self.user)
        token = get_random_string(32)
        self.user.profile.magic_token = token
        self.user.profile.token_created_at = timezone.now()
        self.user.profile.save()
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        url = '/auth/verify-magic-link/' + uid + '/' + token
        request = self.factory.get(url)
        # how to test the expiry of the session?
