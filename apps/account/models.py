from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from datetime import datetime

class UserManager(BaseUserManager):
    def _create(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('User must have first name')
        if not email:
            raise ValueError('User must have email')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        return self._create(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField('Full_name', max_length=255)
    email = models.EmailField('Email', max_length=255, unique=True)
    image = models.ImageField(upload_to='user_images')
    telegram = models.CharField(max_length=255, blank=True, null=True)
    telegram_status = models.BooleanField(default=False)
    position = models.CharField(max_length=100)
    place_of_work = models.CharField(max_length=255)
    about_me = models.CharField(max_length=4096)
    help = models.CharField(max_length=4096)
    level_mentor = models.CharField(max_length=2048)
    experience = models.CharField(max_length=10)
    specialization = models.ManyToManyField(
        to='base.Specialization', 
        related_name='mentor_specialization',
        blank=True
        )
    skills = models.CharField(max_length=512)
    status = models.BooleanField(default=True)
    price = models.CharField(max_length=18)
    language = models.CharField(max_length=20)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return f"{self.username}"

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    def save(self,*args, **kwargs):
        if not self.username:
            raise ValidationError('Поле имени не может быть пустым!')
        super().save(*args, **kwargs)

    def create_activation_code(self):
        code = get_random_string(length=8)
        if User.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = code
        self.save()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'