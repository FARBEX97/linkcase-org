from linkcases import app, db
from linkcases.models import user, linkcase, link

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': user.User, 'Linkcase': linkcase.Linkcase, 'Link': link.Link}