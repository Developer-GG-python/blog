from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)

#CONEXION DE LA DATABASE
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database/blog.db'

db=SQLAlchemy(app)

#--------------------------modelos-------------------------

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50))
    subtitle=db.Column(db.String(50))
    author=db.Column(db.String(20))
    date_posted=db.Column(db.DateTime)
    content=db.Column(db.Text)


class Commentary(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nickname=db.Column(db.String(50))
    content=db.Column(db.Text)
    date_comment=db.Column(db.DateTime)



## VISTAS------------------------
@app.route("/")
def index():
    posts=Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html' , posts=posts)

@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.filter_by(id=post_id).one()
   
    return render_template('post.html',post=post)
@app.route("/contact")
def contact():
    return render_template('contact.html')
## VISTAS------------------------



##ADMIN-------------------

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/admin")
def adminPanel():
    return render_template("admin-panel.html")

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/addpost", methods=['POST'])
def addpost():
    title=request.form['title']
    subtitle=request.form['subtitle']
    author=request.form['author']
    content=request.form['content']

    post=Post(title=title,subtitle=subtitle,author=author,content=content,date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('adminPanel'))
   
@app.route("/views")
def views():
    post=Post.query.all()
    return render_template("views.html", posts=post)

####----------------BORRAR -----------------------
@app.route("/delete/<id>")
def deletePost(id):
    post=Post.query.filter_by(id=int(id)).delete()
    db.session.commit()

    return redirect(url_for('views'))

@app.route("/seach/<id>")
def seach(id):
    post=Post.query.filter_by(id=int(id)).first()

    return render_template("post", posts=post)


@app.route("/edit/<id>")
def editPost(id):
    post=Post.query.filter_by(id=int(id)).first()

    return render_template("edits.html",post=post)





@app.route("/comment")
def commentPost():
    pass




if __name__=="__main__":
    app.run(debug=True)