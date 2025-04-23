from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):  # ✅ Changed to AbstractBaseUser
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_customer = models.BooleanField(default=True)
    is_service_provider = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Needed for admin access
    is_active = models.BooleanField(default=True)  # Needed for authentication

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.full_name

# Profile Model
class Profile(models.Model):
    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("service_provider", "Service Provider"),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.email} - {self.role}"
