from flask import Blueprint
from flask import render_template, request, Blueprint
from flaskblog.models import Posts
main=Blueprint('main',__name__)


@main.route("/")
@main.route("/home")
def home():
    page=request.args.get('page',1,type=int)
    post=Posts.query.order_by(Posts.date.desc()).paginate(page=page,per_page=5)
    return render_template('home.html', posts=post)
# end of register Form

# Start of about Form


@main.route("/about")
def about():
    return render_template('about.html', title='3a4')