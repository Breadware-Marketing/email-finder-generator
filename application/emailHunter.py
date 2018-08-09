from pyhunter import PyHunter
import os

hunter = PyHunter(os.environ.get('email_hunter'))

def get_remaining_calls():
    info = hunter.account_information()
    remaining_calls = info['calls']['left']
    return remaining_calls

def get_domain_personal_email_count(domain):
    info = hunter.email_count(domain=domain)
    personal_email_count = info['personal_emails']
    return personal_email_count

def domain_email_pattern(domain):
    info = hunter.domain_search(domain)
    potential_pattern = info['pattern']
    return potential_pattern

def verify_email(email):
    info = hunter.email_verifier(email)
    result = info['result']

    if result == "undeliverable":
        return None
    elif result == "risky":
        return email
    return email

def guess_email(full_name, domain):
    full_name = full_name.split()
    email_pattern = domain_email_pattern(domain)

    if email_pattern is None:
        return None
    elif email_pattern == '{first}':
        email = full_name[0] + '@' + domain
        return verify_email(email)
    elif email_pattern == '{last}':
        email = full_name[-1] + '@' + domain
        return verify_email(email)
    elif email_pattern == '{f}{last}':
        email = full_name[0][0] + full_name[-1] + '@' + domain
        return verify_email(email)
    elif email_pattern == '{first}{l}':
        email = full_name[0] + full_name[-1][0] + '@' + domain
        return verify_email(email)
    elif email_pattern == '{first}.{last}':
        email = full_name[0] + '.' + full_name[-1] + '@' + domain
        return verify_email(email)
    elif email_pattern == '{first}_{last}':
        email = full_name[0] + '_' + full_name[-1] + '@' + domain
        return verify_email(email)
    elif email_pattern == '{first}{last}':
        email = full_name[0] + full_name[-1] + '@' + domain
        return verify_email(email)
    return email_pattern

def find_email(full_name, domain):
    if not get_remaining_calls():
        return None

    info = hunter.email_finder(full_name=full_name, domain=domain)
    possible_email = info[0]

    if not possible_email:
        return None
    return verify_email(possible_email)
            
