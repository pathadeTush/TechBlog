from flask import render_template, request, Blueprint
from flaskblog.models import Post

# main is the name of package.
main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home', methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('home.html', title='home-page', posts=posts)


@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='about-page')
