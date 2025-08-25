import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email kiritilishi shart!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None 
    email = models.EmailField(unique=True)
    ism = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class CodeVerified(models.Model):
    VIA_EMAIL = "via_email"
    VIA_PHONE = "via_phone"
    AUTH_TYPE = (
        (VIA_EMAIL, "Email orqali"),
        (VIA_PHONE, "Telefon orqali"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="verification_codes")
    code = models.CharField(max_length=6, blank=True, null=True)
    verify_type = models.CharField(max_length=20, choices=AUTH_TYPE)
    expiration_time = models.DateTimeField()
    code_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expiration_time:
            if self.verify_type == self.VIA_EMAIL:
                self.expiration_time = timezone.now() + timedelta(minutes=10)
            elif self.verify_type == self.VIA_PHONE:
                self.expiration_time = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.code_status and timezone.now() <= self.expiration_time

    def __str__(self):
        return f"{self.user.email} - {self.verify_type} - {self.code}"
