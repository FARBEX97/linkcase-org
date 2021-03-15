from workspaces import app, db
from workspaces.models import user, linkcase, link

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': user.User, 'Linkcase': linkcase.Linkcase, 'Link': link.Link}