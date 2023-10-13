from flaskblog.models import Users, Posts
from flask import render_template, url_for, flash, redirect
from flaskblog.form import RegistriationForm, LoginForm
from flaskblog import app,db,bcrypt,login_manager
from flask_login import login_user,current_user,logout_user

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
        return redirect(url_for('home'))
       else:
           flash('wrong input', 'danger')
    return render_template('Login.html', title='Login', form=formm)
# end of Login Form



# Logout route
@app.route("/logout")
def Logout():
   logout_user()
   return redirect(url_for('home'))


@app.route("/Account")
def Account():
     if current_user.is_authenticated:
      return render_template('Account.html',title='Account',user=current_user)
     else:
       return redirect(url_for('login'))