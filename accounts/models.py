from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    """User model manager"""

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Base user class"""
    email = models.EmailField(max_length=255, unique=True)
    is_confirmed = models.BooleanField(
        'confirmed status',
        default=False,
        help_text='Designates whether the user has confirmed its email.',
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_organizer = models.BooleanField(
        'organizer status',
        default=False,
    )
    is_unam_community = models.BooleanField(
        'unam_community status',
        default=True,
    )
    is_active = models.BooleanField(
        'active status',
        default=False,
        help_text=
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.',
    )
    date_joined = models.DateTimeField('date joined', auto_now_add=True)

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class AcademicEntity(models.Model):
    """Academic entity"""
    name = models.CharField(max_length=255, unique=True)


class UserDetail(models.Model):
    """Additional user details"""
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_picture = models.ImageField()
    user = models.OneToOneField(User, models.CASCADE)
    academic_entity = models.ForeignKey(AcademicEntity, models.SET_NULL, null=True)
