from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class AmdUserManager(BaseUserManager):
    """ Manager for the SmdUser manager"""

    def create_user(self, email, password=None):
        """ Create a user """
        if not email:
            raise ValueError(_('Email Field is required'))
        if not password:
            raise ValueError(_('Password is required'))
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, enail, password=None):
        """Create Superuser """
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

