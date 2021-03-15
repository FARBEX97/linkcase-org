from workspaces import db


class Workspace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    links = db.relationship('Link', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f'<Workspace {self.name}>'

        
def get_all_workspaces(user=None):
    """Get a list with all workspaces of a parent user"""
    try:
        return Workspace.query.filter_by(user_id=user.id).all()
    except:
        return None


def get_workspace(workspace_name, user):
    return Workspace.query.filter_by(name=workspace_name, user_id=user.id).first()


def create_workspace(name=None, user=None):
    try:
        workspace = Workspace(name=name, user_id=user.id)
        db.session.add(workspace)
        db.session.commit()
    except:
        pass


def delete_workspace(name=None, user=None):
    try:
        workspace = Workspace.query.filter_by(name=name, user_id=user.id).first()
        db.session.delete(workspace)
        db.session.commit()
    except:
        pass