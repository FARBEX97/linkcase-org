from workspaces import db
from workspaces.models.workspace import Workspace, get_workspace


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    url = db.Column(db.String(64), index=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    
    def __repr__(self):
        return f'<Link {self.name}>'


def create_link(workspace_name=None, user=None, link_url=None, link_name=None):
    try:
        workspace_id = Workspace.query.filter_by(name=workspace_name, user_id=user.id).first().id
        link = Link(name=link_name, url=link_url, workspace_id=workspace_id)
        db.session.add(link)
        db.session.commit()
    except:
        print('Error while creating Link object.')


def delete_link(link_name, parent_workspace_name, user):
    try:
        workspace_id = get_workspace(parent_workspace_name, user).id
        link = Link.query.filter_by(name=link_name, workspace_id=workspace_id).first()
        db.session.delete(link)
        db.session.commit()
    except:
        print('Error while deleting Link object.')

