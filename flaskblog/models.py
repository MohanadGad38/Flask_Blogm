from datetime import datetime
from flaskblog import db
from flaskblog import app,login_manager,LoginManager
from flask_login import UserMixin
# database
# users table
with app.app_context():
    db.create_all()
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
    
class Users(db.Model,UserMixin):
    id:int = db.Column(db.Integer, primary_key=True)
    Username:str = db.Column(db.String(20), unique=True, nullable=False)
    Email:str= db.Column(db.String(20), unique=True, nullable=False, )
    Image_file:str = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password:str = db.Column(db.String(60), nullable=False)
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
