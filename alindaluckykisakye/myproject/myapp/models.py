from django.db import models
from django.contrib.auth.models import AbstractUser

# The CustomUser model extends Django's AbstractUser to add custom fields 
# (full_name, phone_number) required for the signup page.
class CustomUser(AbstractUser):
    
    # Custom fields for the signup form
    full_name = models.CharField(max_length=100, help_text="User's full name.")
    
    # Redefine email and phone_number as unique identifiers
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=10, unique=True, blank=False)
    
    # FIX: Add unique related_name arguments to resolve Django SystemCheck errors 
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups', # Unique name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions', # Unique name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    # By default, AbstractUser uses 'username' for login. 
    # Our views use the email input to populate the AbstractUser's 'username' field 
    # (see signup_view in the Canvas).
    
    def __str__(self):
        return self.email
