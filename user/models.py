from django.core.files.base import ContentFile
from django.core.validators import validate_email
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from urllib import request as request_lib

from user.utils import get_person_detail_based_on_provided_email
from user.validators import custom_validate_email


class User(AbstractUser):
    date_of_birth = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(upload_to='media/users/%Y/%m/%d', blank=True)
    email = models.EmailField(unique=True, validators=[validate_email, custom_validate_email])

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        user_data = get_person_detail_based_on_provided_email(instance.email)
        try:
            instance.first_name = user_data['person']['name']['givenName']
            instance.last_name = user_data['person']['name']['familyName']
        except TypeError:
            pass
        try:
            photo_url = user_data['person']['avatar']
            response = request_lib.urlopen(photo_url)
            image_name = '{}.jpg'.format(slugify(instance.username))
            instance.photo.save(image_name, ContentFile(response.read()))
        except (TypeError, AttributeError):
            pass
