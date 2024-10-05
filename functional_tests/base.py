import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.utils.translation import gettext as _
from authentication.models import CustomUser
import re
import pdb


MAX_WAIT = 5
TEST_NAME = 'Testuser'
TEST_EMAIL = 'toto@example.com'
TEST_PASSWORD = 'XyZzy12345'
SUBJECT = 'Enlace de acceso a afiliacion'


class FunctionalTest(StaticLiveServerTestCase):
    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        cls.test_user = CustomUser.objects.create(username=TEST_NAME, email=TEST_EMAIL)
        cls.test_user.set_password(TEST_PASSWORD)
        cls.test_user.save()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        super().setUp()

    # def tearDown(self):
        # self.browser.quit()
