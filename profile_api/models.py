from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator
# Create your models here.

class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model."""

    def create_user(self, phone_number, name, password=None):
        """Creates a new user profile object."""

        if not phone_number:
            raise ValueError('Users must have an email address.')

        user = self.model(phone_number=phone_number, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, name, password):
        """Creates and saves a new superuser with given details."""

        user = self.create_user(phone_number, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Respents a "user profile" inside our system."""

    phone_regex = RegexValidator(regex=r'09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}', message="شماره تلفن باید به فرمت 09***** باشد")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Used to get a users full name."""

        return self.name + " " + self.last_name

    def get_short_name(self):
        """Used to get a users short name."""

        return self.name

    def __str__(self):
        """Django uses this when it needs to convert the object to a string"""

        return self.name + " " + self.last_name + " " + self.email
