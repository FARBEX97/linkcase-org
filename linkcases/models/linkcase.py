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


def check_if_linkcase_exists(linkcase_name, user):
    linkcase = get_linkcase(linkcase_name, user)
    if linkcase != None:
        return True
    else:
        return False


def check_valid_characters_in_linkcase_name(linkcase_name):
    valid_chars = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz-,. '
    print(linkcase_name)
    for char in linkcase_name:
        if char in valid_chars:
            continue
        else:
            return False
    return True


def normalize_linkcase_name(linkcase_name):
    return linkcase_name.replace(' ', '_')


def create_linkcase(name=None, user=None):
    try:
        name_is_valid = check_valid_characters_in_linkcase_name(name)
        if name_is_valid == False:
            return False
        name = normalize_linkcase_name(name)
        if check_if_linkcase_exists(name, user) == False:
            linkcase = Linkcase(name=name, user_id=user.id)
            db.session.add(linkcase)
            db.session.commit()
            return True
        else:
            return False
    except:
        pass


def delete_linkcase(name=None, user=None):
    try:
        linkcase = Linkcase.query.filter_by(name=name, user_id=user.id).first()
        db.session.delete(linkcase)
        db.session.commit()
    except:
        pass