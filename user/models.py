from django.core.validators import validate_email
from django.db import models
from django.contrib.auth.models import AbstractUser

from user.validators import custom_validate_email


class User(AbstractUser):
    date_of_birth = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    email = models.EmailField(unique=True, validators=[validate_email, custom_validate_email])

    def __str__(self):
        return self.username


