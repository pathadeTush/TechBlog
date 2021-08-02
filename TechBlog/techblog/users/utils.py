# All imports
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from techblog import mail



# Function to save the new profile_picture of the user

def save_picture(form_picture):
    # creating secret key for name of picture filename. we are saving a secret key for picture file instead of saving the name of file directly
    random_hex = secrets.token_hex(8)
    # filename we will not be using furthur so use '_' to store the filename. Because python will throw an error of unused variable. We can avoid it by using underscore.
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # it creates the path by concatenating app path and static/profile_pics folder path with name of file
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics/', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # it saves the picture_path to the argument passed
    i.save(picture_path)

    return picture_fn

# Function to send an email 
def send_reset_email(user):
    token = user.get_reset_token()

    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''
        To reset your password, 
        visit the following link: {url_for('users.reset_token', token=token, _external=True)}
        If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)

#_external=True tells Flask that it should generate an absolute URL, and not a relative URL. For example, https://example.com/my-page is an absolute URL, but /my-page is a relative URL. Since you're sending an email, a relative URL to a page in your site won't work.