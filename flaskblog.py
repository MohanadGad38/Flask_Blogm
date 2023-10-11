from flask import Flask, render_template, url_for, flash, redirect
from datetime import datetime
from form import RegistriationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = 'f6ea78cf69d66fbda36bed5de1694377'
# database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
# craeting database  SQLAlCHEMY


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(20), unique=True, nullable=False)
    Email = db.Column(db.String(20), unique=True, nullable=False, )
    Image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Posts', backref='author', lazy=True)


def __repo__(self):
    return f"users('[self.Username, self.Email, self.Image_file]')"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


def __repo__(self):
    return f"Posts('[self.title, self.date]')"


posts = [
    {
        'author': 'mohanad',
        'title': 'my first post',
        'content': 'hi ',
        'date': 'october 11,2023'
    },
    {
        'author': 'mohanad m',
        'title': 'my second post',
        'content': 'hi ',
        'date': 'october 11,2023'
    }
]

# Start of home Form


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)
# end of register Form

# Start of about Form


@app.route("/about")
def about():
    return render_template('about.html', title='3a4')
# end of register Form
# Start of register Form


@app.route("/register", methods=['GET', 'POST'])
def register():
    formm = RegistriationForm()
    if formm.validate_on_submit():
        flash(f'accout created for {formm.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('Register.html', title='register', form=formm)
# end of register Form
# Start of Login Form


@app.route("/Login", methods=['GET', 'POST'])
def Login():
    formm = LoginForm()
    if formm.validate_on_submit():
        if formm.Email.data == "m@gmail.com" and formm.password.data == "121212":
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('wrong input', 'danger')
    return render_template('Login.html', title='Login', form=formm)
# end of Login Form


# debug mode
if __name__ == '__main__':
    app.run(debug=True)
