import os


class Config:

    # By default, Flask-Login uses sessions for authentication. This means you must set the secret key on your application, otherwise Flask will give you an error message telling you to do so.
    # Flask and some of its extensions use the value of the secret key as a cryptographic key, useful to generate signatures or tokens.
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SECRET_KEY = os.environ.get('SECRET_KEY')  can be generated using another python lib called secrets
    # it will create site.db file in the same folder. It is the file where the data is stored
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
