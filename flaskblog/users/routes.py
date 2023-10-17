from flask import Blueprint
from flaskblog.users.forms import RegistriationForm, LoginForm,UpdateAccountForm,RequestResetForm,ResetPasswordForm
from flaskblog.models import Users, Posts
from flask_login import login_user,current_user,logout_user,login_required
from flaskblog import app,db,bcrypt,login_manager,mail
from flask import render_template, url_for, flash, redirect,request,abort
from PIL import Image
from flaskblog.users.utils import save_picture, send_reset_email
users=Blueprint('users',__name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    formm=RegistriationForm()
    if current_user.is_authenticated:
      return redirect(url_for('main.home'))
      formm = RegistriationForm()
    if formm.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(formm.password.data).decode('utf-8')
        user=Users(Username=formm.username.data,Email=formm.Email.data,password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'accout created you can now login', 'success')
        return redirect(url_for('users.login'))
    return render_template('Register.html', title='register', form=formm)
# end of register Form
# Start of Login Form


@users.route("/login", methods=['GET', 'POST'])


def login():
    if current_user.is_authenticated:
      return redirect(url_for('main.home'))
    formm = LoginForm()
    if formm.validate_on_submit():
       user=Users.query.filter_by(Email=formm.Email.data).first()
       if user and bcrypt.check_password_hash(user.password,formm.password.data):
        login_user(user,remember=formm.remember.data)
        next_page=request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.home'))
       else:
           flash('wrong input', 'danger')
    return render_template('Login.html', title='Login', form=formm)
# end of Login Form



# Logout route
@users.route("/logout")
def logout():
   logout_user()
   return redirect(url_for('main.home'))



@users.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
     elif request.method=='GET':
       formm.username.data=current_user.Username
       formm.Email.data=current_user.Email
       image_file=url_for('static',filename='profile_pic/'+current_user.Image_file)
     image_file=url_for('static',filename='profile_pic/'+current_user.Image_file)  
     if current_user.is_authenticated:
        return render_template('Account.html',title='Account',current_user=current_user,img=image_file,form=formm)
  

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = Users.query.filter_by(Username=username).first_or_404()
    post = Posts.query.filter_by(author=user)\
        .order_by(Posts.date.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_post.html', posts=post, user=user)



@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
   if current_user.is_authenticated:
      return redirect(url_for('main.home'))
   formm=RequestResetForm()
   if formm.validate_on_submit():
      user=Users.query.filter_by(Email=formm.Email.data).first()
      send_reset_email(user)
      flash('an email has been set','info')
      return redirect(url_for('users.login'))
   return render_template('reset_request.html',title='reset password',form=formm)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = Users.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


     
