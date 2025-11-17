# farmers/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class FarmerAccountManager(BaseUserManager):
    def create_user(self, email, first_name='', last_name='', phone_number='', username=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Farmer must have an email address')

        email = self.normalize_email(email)

        # 🔥 Auto-generate username from email if not provided
        if not username:
            username = email.split('@')[0]

        # Ensure username is unique
        original = username
        counter = 1
        while FarmerAccount.objects.filter(username=username).exists():
            username = f"{original}_{counter}"
            counter += 1

        user = FarmerAccount(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name='', last_name='', phone_number='', username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superadmin', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            username=username,
            password=password,
            **extra_fields
        )


class FarmerAccount(AbstractBaseUser, PermissionsMixin):
    first_name    = models.CharField(max_length=50, blank=True)
    last_name     = models.CharField(max_length=50, blank=True)
    username      = models.CharField(max_length=50, unique=True)   # 👉 Restored username
    email         = models.EmailField(max_length=100, unique=True)
    phone_number  = models.CharField(max_length=50, blank=True)

    verified      = models.BooleanField(default=False)
    is_admin      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    date_joined   = models.DateTimeField(default=timezone.now)
    last_login    = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # 👉 Same style as your buyer model

    objects = FarmerAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
