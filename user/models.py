from django.core.files.base import ContentFile
from django.core.validators import validate_email
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from user.utils import get_person_detail_based_on_provided_email
from user.validators import custom_validate_email
from urllib import request as request_lib


class User(AbstractUser):
    date_of_birth = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    email = models.EmailField(unique=True, validators=[validate_email, custom_validate_email])

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def get_additional_info(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(email=instance.email)
        user_data = get_person_detail_based_on_provided_email(instance.email)
        try:
            user.first_name = user_data['person']['name']['givenName']
            user.last_name = user_data['person']['name']['familyName']
        except TypeError:
            pass
        try:
            photo_url = user_data['person']['avatar']
            response = request_lib.urlopen(photo_url)
            image_name = '{}.jpg'.format(slugify(user.username))
            user.photo.save(image_name, ContentFile(response.read()))
        except (TypeError, AttributeError):
            pass
        user.save()

