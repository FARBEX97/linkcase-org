from flask import Flask
import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
if config.dev == True:
    app.config.from_object(config.DevConfig)
else:
    app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from workspaces import routes, models