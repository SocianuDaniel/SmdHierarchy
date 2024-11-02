from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

_MAXLEVEL = 32767
_MINLEVEL = -1

class SmdUserManager(BaseUserManager):
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
        user.level = _MAXLEVEL
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None):
        """Create Superuser """
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.level =_MINLEVEL
        user.save(using=self._db)
        return user
    def create_owner(self, email, password):
        """Create owner """
        user = self.create_user(email, password)
        user.level = 0
        user.save(using=self._db)
        return user
    def create_supervisor(self, email, password, master):
        """create supervisor by a owner """
        if master.level > 0:
            raise ValueError(_('Supervisor must be created by owner'))
        user = self.create_user(email=email, password=password)
        user.master = master
        user.level = 1
        user.save(using=self._db)
        return user


class SmdUser(AbstractBaseUser, PermissionsMixin):
    """User for the project"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    level = models.SmallIntegerField(
        default=_MAXLEVEL,
        validators=[MinValueValidator(_MINLEVEL)])
    master = models.ForeignKey(
        "SmdUser",
        on_delete=models.SET_NULL,
        null=True)
    USERNAME_FIELD = 'email'
    objects = SmdUserManager()


