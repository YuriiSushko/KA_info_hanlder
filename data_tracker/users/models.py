from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models

class MortalsManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Automatically assign the user to their groups and apply permissions
        self.assign_group_permissions(user)
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email, password, and the necessary privileges.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, password, **extra_fields)
        
        # Automatically assign the superuser to their groups and apply permissions
        self.assign_group_permissions(user)
        
        return user

    def assign_group_permissions(self, user):
        """
        Assign permissions to the user based on the groups they belong to.
        """
        for group in user.groups.all():
            # This ensures the user inherits the permissions from the groups
            user.user_permissions.add(*group.permissions.all())
        user.save(using=self._db)


class Mortals(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MortalsManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "Mortal"
        verbose_name_plural = "Mortals"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Roles(Group):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name
