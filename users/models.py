from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models

from common.models import BaseModel
from users.manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):

    class Status(models.TextChoices):
        USER = "US", "User"
        ADMIN = "AD", 'Admin'
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email"), unique=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.USER)
    image = models.ImageField(upload_to='users/', default='users/default-user.png')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # is_superuser = models>BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


    def __str__(self):
        return f"{self.first_name}"
