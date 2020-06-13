from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from Debts.settings import MEDIA_ROOT, STATIC_ROOT
import os
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.save(using=self._db)
        user.is_superuser = True
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name=u'UUID')

    username = models.TextField(unique=True, null=False, blank=True, default='', verbose_name=u'Имя пользователя')
    email = models.EmailField(unique=True, null=False, verbose_name=u'Email пользователя')
    first_name = models.TextField(default='', blank=True, verbose_name=u'Имя')
    last_name = models.TextField(default='', blank=True, verbose_name=u'Фамилия')
    middle_name = models.TextField(default='', blank=True, verbose_name=u'Отчество')

    photo = models.FileField(default=STATIC_ROOT + '/images/user.png', blank=True, null=True, verbose_name=u'Фото')

    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name=u'Время создания')

    is_deleted = models.BooleanField(default=False, verbose_name=u'Удален')
    is_staff = models.BooleanField(default=True, editable=False)
    is_active = models.BooleanField(default=True, editable=False)
    is_superuser = models.BooleanField(default=False, verbose_name=u'Суперюзер (права администратора)')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        ordering = ['is_deleted', 'last_name', 'first_name', 'middle_name', 'created_at']
        db_table = u'Пользователи'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'

    def __str__(self):
        result = self.last_name + ' ' + self.first_name
        if self.middle_name != '':
            result += ' ' + self.middle_name
        if self.is_deleted:
            result += ' - Удален'
        return result

    def server_str(self):
        result = self.last_name + ' ' + self.first_name
        if self.middle_name != '':
            result += ' ' + self.middle_name
        return result

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
