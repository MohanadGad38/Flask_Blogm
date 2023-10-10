from flask import Flask, render_template, url_for
from form import RegistriationForm, LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'f6ea78cf69d66fbda36bed5de1694377'
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


@app.route("/register")
def register():
    formm = RegistriationForm()
    return render_template('Register.html', title='register', form=formm)
# end of register Form
# Start of Login Form


@app.route("/Login")
def Login():
    formm = LoginForm()
    return render_template('Login.html', title='Login', form=formm)
# end of Login Form


# debug mode
if __name__ == '__main__':
    app.run(debug=True)
