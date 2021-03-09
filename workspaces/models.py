from workspaces import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    workspaces = db.relationship('Workspace', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Workspace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    links = db.relationship('Link', backref='workspace', lazy='dynamic')

    def __repr__(self):
        return f'<Workspace {self.name}>'


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    url = db.Column(db.String(64), index=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    
    def __repr__(self):
        return f'<Link {self.name}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))