from flask import Flask, render_template ,request, session
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail

with open('config.json', 'r') as C:
    params = json.load(C)["params"]

local_sever = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'

if(local_sever):
   app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class Contacts(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    msg = db.Column(db.String(120), nullable=False)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    img_file = db.Column(db.String(120), nullable=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)


@app.route("/")
def home():
    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template('index.html', params=params, posts=posts)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if ('user' in session and session['user'] == params['admin_user']):
       return render_template('dashboard.html',params=params)

    if request.method=='POST':
       username = request.form.get('uname')
       userpass = request.form.get('pass')
       if (username == params['admin_user'] and userpass == params['admin_password']):
           session['user'] = username
           return render_template('dashboard.html', params=params)

    return render_template('login.html', params=params)

@app.route("/concert")
def concerts():
    return render_template('concert.html')


@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)


@app.route("/contact",  methods = ['GET', 'POST'])
def contact():
    if (request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        entry = Contacts(name = name,email = email, subject = subject, msg = message,)
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html')

app.run(debug= True)





