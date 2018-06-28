from django.core.exceptions import ValidationError

from user.utils import check_mail_validity_with_never_bounce


def custom_validate_email(value):
    response = check_mail_validity_with_never_bounce(value)
    if response != 'disposable' and response != 'valid':
        raise ValidationError('Please enter a valid email address')
