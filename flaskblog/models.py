from datetime import datetime
from flaskblog import db
from flaskblog import app
# database
# users table
with app.app_context():
    db.create_all()


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

# posts table


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


def __repo__(self):
    return f"Posts('[self.title, self.date]')"
