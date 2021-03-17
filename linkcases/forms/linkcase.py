from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



class NewLinkcaseForm(FlaskForm):
    linkcase_name = StringField('New Linkcase', validators=[DataRequired()], render_kw={"placeholder": "New Linkcase"})
    submit = SubmitField('+')


class DeleteLinkcaseForm(FlaskForm):
    delete = SubmitField('Delete')