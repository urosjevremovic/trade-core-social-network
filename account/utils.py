import requests
import clearbit

email_hunter_api_key = 'a75f1f551634d70884f8c059160c1a455b4bfb46'
email_hippo_api_key = '011EEB7F'
clearbit.key = 'sk_8bd5becf75c9824855a6d6a23f957c0a'


def check_mail_validity_with_email_hunter(mail):
    response = requests.get(f'https://api.hunter.io/v2/email-verifier?email={mail}&api_key={email_hunter_api_key}').\
        json()
    return response['data']['result']


check_mail_validity_with_email_hunter('urosh43@gmail.com')


def check_mail_validity_with_email_hippo(mail):
    response = requests.get(f'https://api1.27hub.com/api/emh/a/v2?k={email_hippo_api_key}&e={mail}').json()
    return response['result']


def get_person_detail_based_on_provided_email(mail):
    person = clearbit.Person.find(email=mail, stream=True)
    if person is not None:
        return person
