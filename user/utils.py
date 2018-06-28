from urllib.parse import quote

import requests
import json


with open('api_keys.json') as f:
    api_keys = json.load(f)

never_bounce_api_key = api_keys['never_bounce_api_key']


def check_mail_validity_with_never_bounce(mail):
    parsed_email = quote(mail)
    response = requests.get(f'https://api.neverbounce.com/v4/single/check?key={never_bounce_api_key}'
                            f'&email={parsed_email}').json()
    try:
        return response['result']
    except KeyError:
        print('Reached maximum daily number of email verification checks.')
        pass
