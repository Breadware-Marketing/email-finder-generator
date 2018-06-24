import requests
import json
import os
from . import emailHunter

api_key = os.environ.get('prospect.io')

def split_name(full_name):
    return full_name.split()

def verify(email):
    verify_url = 'https://prospect.io/api/public/v1/emails/verify?'
    headers = {'Authorization': api_key}
    email = 'email=' + email

    r = requests.get(verify_url + email, headers=headers)
    return(json.loads(r.text))

def find_email(full_name, domain):
    find_url = 'https://prospect.io/api/public/v1/emails/search?'
    headers = {'Authorization': api_key}

    domain = 'domain=' + domain
    full_name = split_name(full_name)
    first_name = '&first_name=' + full_name[0]
    last_name = '&last_name=' + full_name[-1]

    r = requests.get(find_url + domain + first_name + last_name, headers=headers)
    data = json.loads(r.text)

    try:
        email = data['data'][0]['attributes']['value']
        if emailHunter.verify_email(email):
            return email
        return None
    except:
        return None