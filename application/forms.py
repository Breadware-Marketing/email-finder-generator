from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class EmailForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    company_url = StringField('Company Website', validators=[DataRequired()])
    submit = SubmitField('Find Email')