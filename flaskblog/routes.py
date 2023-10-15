import time
import secrets
from PIL import Image
from flaskblog.models import Users, Posts
from flask import render_template, url_for, flash, redirect,request
from flaskblog.form import RegistriationForm, LoginForm,UpdateAccountForm
from flaskblog import app,db,bcrypt,login_manager
from flask_login import login_user,current_user,logout_user,login_required
import os
# craeting database  SQLAlCHEMY
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
    formm=RegistriationForm()
    if current_user.is_authenticated:
      return redirect(url_for('home'))
      formm = RegistriationForm()
    if formm.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(formm.password.data).decode('utf-8')
        user=Users(Username=formm.username.data,Email=formm.Email.data,password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'accout created you can now login', 'success')
        return redirect(url_for('login'))
    return render_template('Register.html', title='register', form=formm)
# end of register Form
# Start of Login Form


@app.route("/login", methods=['GET', 'POST'])


def login():
    if current_user.is_authenticated:
      return redirect(url_for('home'))
    formm = LoginForm()
    if formm.validate_on_submit():
       user=Users.query.filter_by(Email=formm.Email.data).first()
       if user and bcrypt.check_password_hash(user.password,formm.password.data):
        login_user(user,remember=formm.remember.data)
        next_page=request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('home'))
       else:
           flash('wrong input', 'danger')
    return render_template('Login.html', title='Login', form=formm)
# end of Login Form



# Logout route
@app.route("/logout")
def logout():
   logout_user()
   return redirect(url_for('home'))

def save_picture(form_picture):
   random_hex=secrets.token_hex(8)
   _,f_ext=os.path.splitext(form_picture.filename)
   picture_fn=random_hex+f_ext
   picture_path=os.path.join(app.root_path,'static/profile_pic',picture_fn)
   output=[125,125]
   i=Image.open(form_picture)
   i.thumbnail(output)

   i.save(picture_path)
   return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
     formm=UpdateAccountForm()
     if formm.validate_on_submit():
        if formm.picture.data:
           picture_file=save_picture(formm.picture.data)
           current_user.Image_file=picture_file
        current_user.Username=formm.username.data
        current_user.Email=formm.Email.data
        db.session.commit()
        flash('success nice ', 'success')
        return redirect(url_for('account'))
     elif request.method=='GET':
       formm.username.data=current_user.Username
       formm.Email.data=current_user.Email
       image_file=url_for('static',filename='profile_pic/'+current_user.Image_file)
     image_file=url_for('static',filename='profile_pic/'+current_user.Image_file)  
     if current_user.is_authenticated:
        return render_template('Account.html',title='Account',current_user=current_user,img=image_file,form=formm)
  




@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
   return render_template('create_post.html',title='create post')
   