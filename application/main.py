from flask import Flask, render_template, flash, redirect
from .forms import EmailForm
import os
from . import emailHunter
from . import emailProspect
from urllib.parse import urlparse
from flask import jsonify, request

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY=  os.environ.get('SECRET_KEY'),
    WTF_CSRF_SECRET_KEY=  os.environ.get('WTF_CSRF_SECRET_KEY')
))

def clean_url(domain):
    domain = urlparse(domain)
    domain = domain.netloc if domain.netloc else domain.path

    if "www." in domain:
        domain = domain[4:]
    return domain

def generate_email(full_name, domain):
    domain = clean_url(domain)

    if not emailHunter.get_remaining_calls():
        return "Need To Upgrade Account"

    if emailHunter.find_email(full_name, domain):
        return emailHunter.find_email(full_name, domain)
    elif emailProspect.find_email(full_name, domain):
        return emailProspect.find_email(full_name, domain)
    return emailHunter.guess_email(full_name, domain)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm()
    if form.validate_on_submit():
        email_result = generate_email(str(form.full_name.data), str(form.company_url.data))
        flash('{}'.format(email_result))
        return redirect('/')
    return render_template('main.html', title='Find Email', form=form)

@app.route('/api', methods=['GET'])
def api():
    if 'name' in request.args and 'url':
        email_result = generate_email(str(request.args['name']), str(request.args['url']))
        return jsonify(
            email=email_result
            )

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)