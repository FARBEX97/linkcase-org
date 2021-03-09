from workspaces import app, db
from workspaces.models import User, Workspace, Link

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Workspace': Workspace, 'Link': Link}