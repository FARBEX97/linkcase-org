from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



class NewWorkspaceForm(FlaskForm):
    ws_name = StringField('Workspace', validators=[DataRequired()])
    submit = SubmitField('Create')


class DeleteWorkspaceForm(FlaskForm):
    delete = SubmitField('Delete')