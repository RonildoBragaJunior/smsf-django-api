# import requests

MAILGUN_DOMAIN_NAME = 'squirrelsuper.com.au'
MAILGUN_API_KEY = 'd4a62ee74f4d93e4e6bb92e27e1a4b77-6b60e603-dec213b5'

def send_account_activation(to):
    url = 'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN_NAME)

    f = open('resources/templates/account_activation/content.txt','r')

    data = {
        'from': 'Mailgun User <save@{}>'.format(MAILGUN_DOMAIN_NAME),
        'to': to,
        'subject': 'Squirrel account activation',
        'text': f.read(),
    }

    # requests.post(url, auth=('api', MAILGUN_API_KEY), data=data)
