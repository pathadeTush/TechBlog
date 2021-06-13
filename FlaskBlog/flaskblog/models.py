from flaskblog import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


# You will need to provide a user_loader callback. This callback is used to reload the user object from the user ID stored in the session. It should take the unicode ID of a user, and return the corresponding user object.

@login_manager.user_loader
def load_user(user_id):
    # It should return None (not raise an exception) if the ID is not valid. (In that case, the ID will manually be removed from the session and processing will continue.)
    return User.query.get(int(user_id))


''' The baseclass for all your models is called db.Model. It’s stored on the SQLAlchemy instance that we have created. Which 'db' see __init__.py file

 some parts that are required in SQLAlchemy are optional in Flask-SQLAlchemy. For instance the table name is automatically set for you unless overridden. It’s derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case”. To override the table name, set the __tablename__ class attribute. You can check tabelname on interpreter as User.query.all()[1].__tablename__

 UserMixin model is used to handel user sessions like is_active, is_anonymous, is_authenticated, get_id(). It provides default implementations for all of these properties and methods. (It’s not required, though.)'''


class User(db.Model, UserMixin):
    # primary key is used because it is needed for SQLAlchemy to convert / map python classes (here User and Post) to the table and to access a specific object, every object needs there to be at least one column denoted as a primary key column. We can access any object using this column. Here this column is 'id'.
    id = db.Column(db.Integer, primary_key=True)

    # nullable=False implies this field can't be empty
    username = db.Column(db.String(20), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')

    password = db.Column(db.String(60), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)

    ''' relationship defines relationship with class Post with posts variable which is a data member of a User Class
 Implies each User created has data member posts which is related with another class named Post and we can access all posts of that user via posts data member

backref adds another column in database here it is 'author'.We can access posts using author.lazy = True means this relationship is supposed to load in one go

To know more about lazy=True  visit:- https://medium.com/@ns2586/sqlalchemys-relationship-and-lazy-parameter-4a553257d9ef
'''

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        # gives sectret key for user_id
        return s.dumps({'user_id': self.id}).decode('utf-8')

# for static methods we don't need self argument
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # gives the user id of user if the given seconds hasn't expired
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

# repr gives the object as a string

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    # datetime.utcnow gives current time
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # User class has one table named user.id
    # 'user'(lowercase of class name User) is name of table by default  if not set manually. In that table there is row named 'id'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
