from workspaces import db
from workspaces.models.linkcase import Linkcase, get_linkcase


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    url = db.Column(db.String(64), index=True)
    linkcase_id = db.Column(db.Integer, db.ForeignKey('linkcase.id'))
    
    def __repr__(self):
        return f'<Link {self.name}>'


def create_link(linkcase_name=None, user=None, link_url=None, link_name=None):
    try:
        linkcase_id = Linkcase.query.filter_by(name=linkcase_name, user_id=user.id).first().id
        link = Link(name=link_name, url=link_url, linkcase_id=linkcase_id)
        db.session.add(link)
        db.session.commit()
    except:
        print('Error while creating Link object.')


def delete_link(link_name, parent_linkcase_name, user):
    try:
        linkcase_id = get_linkcase(parent_linkcase_name, user).id
        link = Link.query.filter_by(name=link_name, linkcase_id=linkcase_id).first()
        db.session.delete(link)
        db.session.commit()
    except:
        print('Error while deleting Link object.')

