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
    form = PostForm()

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
    # returns a post or 404 error by the post_id
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# update post route
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
# required an integer post_id
def update_post(post_id):
    # returns a post or 404 error by the post_id
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
