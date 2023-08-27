from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
# Create your models here.
class UserManager(BaseUserManager):
  

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    user_roles= [('user', 'user'), ('admin', 'admin')]
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices= user_roles, default='user')
    date_joined = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(Group, blank=True, related_name="custom_users")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="custom_users")

    USERNAME_FIELD = 'email'		
    REQUIRED_FIELDS = ['full_name', 'email', 'is_staff', 'role']

    objects = UserManager()

    def __str__(self):
        return self.email
   