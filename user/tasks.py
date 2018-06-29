from celery import task
from django.core.files.base import ContentFile
from django.utils.text import slugify

from urllib import request as request_lib

from user.models import User
from user.utils import get_person_detail_based_on_provided_email


@task
def additiona_info_about_user(id):
    user = User.objects.get(id=id)
    user_data = get_person_detail_based_on_provided_email(user.email)
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