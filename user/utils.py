from urllib.parse import quote

import requests
import json
import clearbit


with open('api_keys.json') as f:
    api_keys = json.load(f)

never_bounce_api_key = api_keys['never_bounce_api_key']
clearbit.key = api_keys['clearbit_api_key']


def check_mail_validity_with_never_bounce(mail):
    parsed_email = quote(mail)
    response = requests.get(f'https://api.neverbounce.com/v4/single/check?key={never_bounce_api_key}'
                            f'&email={parsed_email}').json()
    try:
        return response['result']
    except KeyError:
        print('Reached maximum daily number of email verification checks.')
        pass


def get_person_detail_based_on_provided_email(mail):
    person = clearbit.Enrichment.find(email=mail, stream=True)
    if person is not None:
        return person