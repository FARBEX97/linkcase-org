from linkcases import db


class Linkcase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    links = db.relationship('Link', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f'<Linkcase {self.name}>'


def get_all_linkcases(user=None):
    """Get a list with all linkcases of a parent user"""
    try:
        return Linkcase.query.filter_by(user_id=user.id).all()
    except:
        return None


def get_linkcase(linkcase_name, user):
    return Linkcase.query.filter_by(name=linkcase_name, user_id=user.id).first()


def create_linkcase(name=None, user=None):
    try:
        linkcase = Linkcase(name=name, user_id=user.id)
        db.session.add(linkcase)
        db.session.commit()
    except:
        pass


def delete_linkcase(name=None, user=None):
    try:
        linkcase = Linkcase.query.filter_by(name=name, user_id=user.id).first()
        db.session.delete(linkcase)
        db.session.commit()
    except:
        pass