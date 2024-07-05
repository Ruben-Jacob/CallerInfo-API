from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, name, phone_number, password=None, email=None):
        if not name:
            raise ValueError('Users must have a name')
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            name=name,
            phone_number=phone_number,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, phone_number, password, email=None):
        user = self.create_user(
            name=name,
            phone_number=phone_number,
            password=password,
            email=email,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=15, 
        unique=True, 
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')]
    )
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']
    
    @property
    def is_staff(self):
        return self.is_admin

class Spam(models.Model):
    phone_number = models.CharField(max_length=15)
    marked_by = models.ForeignKey(User, related_name='marked_spams', on_delete=models.CASCADE)

    def __str__(self):
        return f"Spam: {self.phone_number} (Marked by: {self.marked_by.name})"
