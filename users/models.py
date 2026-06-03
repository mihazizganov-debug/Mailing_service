from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="телефон")
    avatar = models.ImageField(upload_to="users/", blank=True, null=True, verbose_name="аватар")
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name="страна")
    is_active = models.BooleanField(default=True, verbose_name="активен")
    is_blocked = models.BooleanField(default=False, verbose_name="заблокирован")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()  # 👈 добавить

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.email
