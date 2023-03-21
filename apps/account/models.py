from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError


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
    username = models.CharField('Full_name', max_length=50, blank=True)
    email = models.EmailField('Email', max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to='user_images', blank=True)
    position = models.CharField(max_length=100, blank=True)
    place_of_work = models.CharField(max_length=255, blank=True)
    about_me = models.CharField(max_length=255, blank=True)
    help = models.CharField(max_length=255, blank=True)
    level_mentor = models.CharField(max_length=255, blank=True)
    experience = models.CharField(max_length=255, blank=True )
    speciality = models.CharField(max_length=255, blank=True)
    skills = models.CharField(max_length=255, blank=True)

    type_price = [
        ('Negotiable', 'Договорно'),
        ('For free', 'Бесплатно'),
        ('1000 сом', '1000 RUB'),
        ('2000 сом', '2000 RUB'),
        ('3000 сом', '3000 RUB'),
        ('4000 сом', '4000 RUB'),
        ('5000 сом', '5000 RUB'),
        ('6000 сом', '6000 RUB'),
        ('7000 сом', '7000 RUB'),
        ('8000 сом', '8000 RUB'),
        ('9000 сом', '9000 RUB' ),
        ('10000 сом','10000 RUB'),
    ]

    price = models.CharField(choices=type_price, max_length=255, blank=True)
    stacks = models.CharField(max_length=255, blank=True)
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



