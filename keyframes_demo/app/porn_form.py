from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class PornForm(Form):
    url = StringField('url', validators=[DataRequired()])
