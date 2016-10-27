from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class CopyForm(Form):
    url_a = StringField('url_a', validators=[DataRequired()])
    url_b = StringField('url_b', validators=[DataRequired()])
