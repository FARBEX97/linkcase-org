from workspaces import app, db
from workspaces.models import user, workspace, link

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': user.User, 'Workspace': workspace.Workspace, 'Link': link.Link}