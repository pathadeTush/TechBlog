# All imports required

import datetime
from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

# Creating bluepring of posts
posts = Blueprint('posts', __name__)

# new_post route with GET and POST method and login_required decorator
@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    # instance of PostForm
    form = PostForm() # to know how it works go to bottom of this page or go to https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

    # Validating the credentials of the form 
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        # Saving the new post to the db
        db.session.add(post)
        db.session.commit()
        
        # Putting alert on the user end and a bootstrap success call 
        flash('Your new Post has been created!', 'success')
        
        # redirecting back to homepage
        return redirect(url_for('main.home'))

    # if an invalid form re-render the html
    return render_template('create_post.html', title='New-Post', form=form, legend='New Post')


# post route
@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
# required an integer post_id
def post(post_id):
    # returns a post object having id of post as 'post_id'.
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# update post route
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
# required an integer post_id
def update_post(post_id):
    # returns a post object having id of post as 'post_id'.
    post = Post.query.get_or_404(post_id)
    
    # if not the user's post
    if post.author != current_user:
        # abort by returning 403
        abort(403)
    
    form = PostForm()
    # Validating the credentials of the form 
    if form.validate_on_submit():
        # Saving changes to db
        post.title = form.title.data
        post.content = form.content.data
        post.date_posted = datetime.utcnow()
        db.session.commit()
        
        # alert for user
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))

    # if the request is just 'GET' then just render the prev data in the form as it is
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update-Post', form=form, legend='Update Post')

# delete_post route, login_required decorator
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
# needs an integer post_id
def delete_post(post_id):
    # gets the post or return 404 if not found 
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        # if user is not author return 403
        abort(403)

    # Removing the post after validation and saving changes to db
    db.session.delete(post)
    db.session.commit()

    flash('Your post has been deleted!', 'success')
    # redirecting to home again
    return redirect(url_for('main.home'))



'''
The first new thing in this version is the methods argument in the route decorator. This tells Flask that this view function accepts GET and POST requests, overriding the default, which is to accept only GET requests. The HTTP protocol states that GET requests are those that return information to the client (the web browser in this case). All the requests in the application so far are of this type. POST requests are typically used when the browser submits form data to the server (in reality GET requests can also be used for this purpose, but it is not a recommended practice). The "Method Not Allowed" error that the browser showed you before, appears because the browser tried to send a POST request and the application was not configured to accept it. By providing the methods argument, you are telling Flask which request methods should be accepted.

The form.validate_on_submit() method does all the form processing work. When the browser sends the GET request to receive the web page with the form, this method is going to return False, so in that case the function skips the if statement and goes directly to render the template in the last line of the function.

When the browser sends the POST request as a result of the user pressing the submit button, form.validate_on_submit() is going to gather all the data, run all the validators attached to fields, and if everything is all right it will return True, indicating that the data is valid and can be processed by the application. But if at least one field fails validation, then the function will return False, and that will cause the form to be rendered back to the user, like in the GET request case. Later I'm going to add an error message when validation fails.

When form.validate_on_submit() returns True, the login view function calls two new functions, imported from Flask. The flash() function is a useful way to show a message to the user. A lot of applications use this technique to let the user know if some action has been successful or not. In this case, I'm going to use this mechanism as a temporary solution, because I don't have all the infrastructure necessary to log users in for real yet. The best I can do for now is show a message that confirms that the application received the credentials.
'''