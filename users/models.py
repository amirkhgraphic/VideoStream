from PIL import Image
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    avatar = models.ImageField(default='default/avatar.png', upload_to='avatar/')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            avatar_path = self.avatar.path
            with Image.open(avatar_path) as img:
                width, height = img.size
                if width != height:
                    new_dimension = min(width, height)
                    left = (width - new_dimension) / 2
                    top = (height - new_dimension) / 2
                    right = (width + new_dimension) / 2
                    bottom = (height + new_dimension) / 2
                    img = img.crop((left, top, right, bottom))

                img.save(avatar_path)

    def __str__(self):
        return f"@{self.username}"
