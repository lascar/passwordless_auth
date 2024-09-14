from django.utils.translation import gettext as _
import re
import pdb
from selenium.webdriver.common.by import By
from django.core import mail
from .base import FunctionalTest

TEST_EMAIL = 'toto@example.com'
SUBJECT = _('Your magic login link')

class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        self.browser.get(self.live_server_url + '/auth/send-magic-link/')
        self.browser.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        self.wait_for(lambda: self.assertIn(
            _('A magic link has been sent to your email.'),
            self.browser.find_element(By.TAG_NAME, 'body').text
        ))

        email = mail.outbox[0]  
        self.assertIn(TEST_EMAIL, email.to)
        print('email.subject')
        print(email.subject)
        self.assertEqual(email.subject, SUBJECT)

        self.assertIn(_('Click the link below to log in'), email.body)
        # http://localhost:59375/auth/verify-magic-link/MQ/1yq3KcK7xDszO7JoaaKFjuJjmjyTgZoz
        url_search = re.search(r'http://.+/', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        self.browser.get(url)
