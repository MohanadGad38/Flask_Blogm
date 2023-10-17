from dotenv import load_dotenv
import os
load_dotenv('/Users/mohanadgad/bash_profile.env')
class Config:
  
  SECRET_KEY=os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
  MAIL_SERVER = 'smtp.googlemail.com'
  MAIL_PORT = 587
  MAIL_USE_TLS= True
  MAIL_PASSWORD=os.environ.get('PASS_M')
  MAIL_USERNAME = os.environ.get('EMAIL_M')
  


