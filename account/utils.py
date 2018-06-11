import requests
import clearbit
import random
import string
import json

"""
For testing purposes only, if this was an actual production app or if local environment was run only on my
machine, these values would be saved as environment variables.
"""

with open('api_keys.json') as f:
    api_keys = json.load(f)

email_hunter_api_key = api_keys['email_hunter_api_key']
email_hippo_api_key = api_keys['email_hippo_api_key']
never_bounce_api_key = api_keys['never_bounce_api_key']
clearbit.key = api_keys['clearbit_api_key']


def check_mail_validity_with_email_hunter(mail):
    response = requests.get(f'https://api.hunter.io/v2/email-verifier?email={mail}&api_key={email_hunter_api_key}').\
        json()
    try:
        return response['data']['result']
    except KeyError:
        print('Reached maximum daily number of email verification checks.')
        pass


def check_mail_validity_with_email_hippo(mail):
    response = requests.get(f'https://api1.27hub.com/api/emh/a/v2?k={email_hippo_api_key}&e={mail}').json()
    try:
        return response['result']
    except KeyError:
        print('Reached maximum daily number of email verification checks.')
        pass


def check_mail_validity_with_never_bounce(mail):
    response = requests.get(f'https://api.neverbounce.com/v4/single/check?key={never_bounce_api_key}&email={mail}').json()
    try:
        return response['result']
    except KeyError:
        print('Reached maximum daily number of email verification checks.')
        pass


def get_person_detail_based_on_provided_email(mail):
    person = clearbit.Person.find(email=mail, stream=True)
    if person is not None:
        return person


def code_generator(size=15, chars=string.ascii_lowercase + string.digits):

    return ''.join(random.choice(chars) for _ in range(size))
