# All imports

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config




# SQLAlchemy is a library that facilitates the communication between Python programs and databases. Most of the times, this library is used as an Object Relational Mapper (ORM) tool that translates Python classes to tables on relational databases and automatically converts function calls to SQL statements.
db = SQLAlchemy()

# bcrypt is used for hash code generation for password and password varification
bcrypt = Bcrypt()

# The login manager contains the code that handels the user's session details, such as how to load a user from an ID, where to send users when they need to log in, and the like.


login_manager = LoginManager()

# By default, when a user attempts to access a login_required view without being logged in, Flask-Login will flash a message and redirect them to the log in view. (If the login view is not set, it will abort with a 401 error.)

login_manager.login_view = 'users.login'    # login is name of function
login_manager.login_message_category = 'info'

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # importing users, posts, errors, main blueprints

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    
    # making blueprints registered and intact
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # initializing the export variables 
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    return app

