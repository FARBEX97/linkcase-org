from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired



class NewLinkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    url = StringField('Url', validators=[DataRequired()])
    workspace = SelectField('Workspace', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Add Link')