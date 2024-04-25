from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone



class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class UserData(AbstractUser):

    username = None
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name



class Calculation(models.Model):
    OPERATION_CHOICES = [
        ('add', 'Addition'),
        ('subtract', 'Subtraction'),
        ('multiply', 'Multiplication'),
        ('divide', 'Division'),
    ]

    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES)
    operand1 = models.FloatField()
    operand2 = models.FloatField()
    result = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.operation} {self.operand1} {self.operand2} = {self.result}"

    def save(self, *args, **kwargs):
        try:
            if self.operation == 'add':
                self.result = self.operand1 + self.operand2
            elif self.operation == 'subtract':
                self.result = self.operand1 - self.operand2
            elif self.operation == 'multiply':
                self.result = self.operand1 * self.operand2
            elif self.operation == 'divide':
                if self.operand2 != 0:
                    self.result = self.operand1 / self.operand2
                else:
                    self.result = None  # Handle division by zero error
            else:
                self.result = None  # Handle invalid operation error
        except Exception as e:
            self.result = None  # Handle any other unexpected errors
            # Optionally, log the exception for debugging purposes
            print(f"An error occurred during calculation: {e}")

        super().save(*args, **kwargs)