from datetime import datetime
from flaskblog import db
from flaskblog import app,login_manager,LoginManager,app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
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
    Email:str= db.Column(db.String(100), unique=True, nullable=False, )
    Image_file:str = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password:str = db.Column(db.String(60), nullable=False)
    post = db.relationship('Posts', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)

    def __repr__(self):
        return f"User('{self.Username}', '{self.Email}', '{self.Image_file}')"

# posts table


class Posts(db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    title:str = db.Column(db.String(100), nullable=False)
    date:datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content:str = db.Column(db.Text, nullable=False)
    user_id:int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


def __repo__(self):
    return f"Posts('[self.title, self.date]')"
