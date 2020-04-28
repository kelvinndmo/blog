from flask import Blueprint, request, render_template
from models.models import Post

main = Blueprint('main', __name__)


@main.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(per_page=4, page=page)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html')
