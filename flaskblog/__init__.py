
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f6ea78cf69d66fbda36bed5de1694377'
# database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_M')
#app.config['MAIL_PASSWORD'] = os.environ.get('PASS_M')
print(os.environ.get('EMAI_M'))
print(os.environ.get('PASS_M'))
print(os.environ)

mail = Mail(app)

with app.app_context():
    db.create_all()

from flaskblog import routes