from flask import render_template, request, Blueprint
from flaskblog.models import Post

# main is the name of package.
main = Blueprint('main', __name__)


# root route or home route
@main.route('/')
@main.route('/home', methods=['GET', 'POST'])
def home():
    # pagination 
    page = request.args.get('page', 1, type=int)

    # ordering the post in descending order of date_posted so as newest is at top
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('home.html', title='home-page', posts=posts)


# about page route
@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='about-page')


# latest posts routes

@main.route('/latest_post')
def latest_post():
    # getting all the posts 
    posts = Post.query.order_by(Post.date_posted.desc())
    # reversing the posts so as to get the latest at top
    return render_template('latest_post.html', title='Latest-post', posts = posts)

# calendar route
@main.route('/calendar')
def calendar():
    # renders an html for a calendar element
    return render_template('calender.html', title='Calendar')

# annnouncement route
@main.route('/announcements')
def announcements():
    return render_template('announcements.html', title='Announcements')
