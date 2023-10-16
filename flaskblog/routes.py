import time
import secrets
from PIL import Image
from flaskblog.models import Users, Posts
from flask import render_template, url_for, flash, redirect,request,abort
from flaskblog.form import RegistriationForm, LoginForm,UpdateAccountForm,Postform
from flaskblog import app,db,bcrypt,login_manager
from flask_login import login_user,current_user,logout_user,login_required
import os
# craeting database  SQLAlCHEMY

# Start of home Form


@app.route("/")
@app.route("/home")
def home():
    page=request.args.get('page',1,type=int)
    post=Posts.query.order_by(Posts.date.desc()).paginate(page=page,per_page=5)
    return render_template('home.html', posts=post)
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
   formm=Postform()
   if formm.validate_on_submit():
   
        post=Posts(title=formm.title.data,content=formm.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("posted",'success')
        return redirect(url_for('home'))
   return render_template('create_post.html',title='create post',form=formm,legend="New post")
   
   
@app.route("/post/int:<Posts_id>")
def post(Posts_id):
   post=Posts.query.get_or_404(Posts_id)
   return render_template('post.html',title=post.title,post=post)
   

  

@app.route("/post/int:<Posts_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(Posts_id):
   post=Posts.query.get_or_404(Posts_id)
   if post.author!=current_user:
      abort(403)
   formm=Postform()
   if formm.validate_on_submit():
     post.title=formm.title.data
     post.content=formm.content.data
     db.session.commit()
     flash("updated","success")
     return redirect(url_for('post',Posts_id=post.id))
   elif request.method=='GET':
    formm.title.data=post.title
    formm.content.data=post.content
   return render_template('create_post.html',title='upadte post',form=formm,legend="update post")

@app.route("/post/int:<Posts_id>/delete", methods=[ 'POST'])
@login_required
def delete_post(Posts_id):
 post=Posts.query.get_or_404(Posts_id)
 if post.author!=current_user:
      abort(403)
 db.session.delete(post)
 db.session.commit()
 flash('your post has been deleted','success')
 return redirect(url_for('home'))




@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = Users.query.filter_by(Username=username).first_or_404()
    post = Posts.query.filter_by(author=user)\
        .order_by(Posts.date.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_post.html', posts=post, user=user)