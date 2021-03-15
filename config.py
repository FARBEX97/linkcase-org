import os
basedir = os.path.abspath(os.path.dirname(__file__))
dev = True

class DevConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'linkcaseorg.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'