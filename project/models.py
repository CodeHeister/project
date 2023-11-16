import bcrypt
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from datetime import datetime
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, name, username, password=None):
        if not name or not username:
            raise ValueError('Users must have an email address')

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, name, username, password):
        user = self.create_user(
            name,
            username,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, name, username, password):
        user = self.create_user(
            name,
            username,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(default=datetime.now, blank=True)
    is_active = models.BooleanField(default = True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
