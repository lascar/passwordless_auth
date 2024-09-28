from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext as _
import pdb

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username.strip(), email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        # breakpoint()
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits, and spaces only.'),
        validators=[],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    objects = CustomUserManager()

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)
    magic_token = models.CharField(max_length=64, blank=True, null=True)
    token_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def is_token_expired(self):
        return self.token_created_at < timezone.now() - timedelta(minutes=15)


