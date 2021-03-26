from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired



class NewLinkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={'placeholder': 'Name'})
    url = StringField('Url', validators=[DataRequired()], render_kw={'placeholder': 'Url'})
    # workspace = SelectField('Workspace', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Add')