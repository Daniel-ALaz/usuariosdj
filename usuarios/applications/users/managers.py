from django.db import models

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff, # viene en el AbstractBaseUser
            is_superuser=is_superuser, # viene en el AbstractBaseUser
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db) # using es para especificar en que bbdd
        return user
    #def create_user

    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True, True, **extra_fields) # los 'True' son por los is staff y superuser