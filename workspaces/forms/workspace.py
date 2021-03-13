from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



class NewWorkspaceForm(FlaskForm):
    ws_name = StringField('New Workspace', validators=[DataRequired()], render_kw={"placeholder": "New Workspace"})
    submit = SubmitField('Create Workspace')


class DeleteWorkspaceForm(FlaskForm):
    delete = SubmitField('Delete')