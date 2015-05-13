from flask import render_template

from blog import app
from .database import session
from .models import Post

from flask import flash
from flask.ext.login import login_user
from werkzeug.security import check_password_hash
from .models import User

from flask.ext.login import login_required

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
  # Zero-indexed page
  page_index = page - 1
  
  # To determine how many items there are in total
  count = session.query(Post).count()
  
  # The index of the first/last item that should be seen
  start = page_index * paginate_by
  end = start + paginate_by
  
  # The total number of pages of content
  # Whether there is a page after/before the current page
  total_pages = (count - 1) / paginate_by + 1
  has_next = page_index < total_pages - 1
  has_prev = page_index > 0
  
  posts = session.query(Post)
  posts = posts.order_by(Post.datetime.desc())
  posts = posts[start:end]
  
  return render_template("posts.html", 
                        posts=posts,
                        has_next=has_next,
                        has_prev=has_prev,
                        page=page,
                        total_pages=total_pages
                        )


@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
  # Route will only be used for GET requests to the page
  return render_template("add_post.html")


import mistune
from flask import request, redirect, url_for


@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
  # Route for the POST request during form submission
  post = Post(
    title=request.form["title"],
    content=mistune.markdown(request.form["content"]),
  )
  session.add(post)
  session.commit()
  
  # Send user back to the front page after post is created
  return redirect(url_for("posts"))


@app.route("/post/<int:id>")
def view_post(id):
  # Route for single post view by clicking post title
  post = session.query(Post).get(id)
  return render_template("single_post.html", 
                        post=post)


@app.route("/post/<int:id>/edit", methods=["GET"])
def edit_post_get(id):
  post = session.query(Post).get(id)
  return render_template("edit_post.html", post=post)


@app.route("/post/<int:id>/edit", methods=["POST"])
def edit_post_post(id):
  post = session.query(Post).get(id)
  post.title = request.form["title"],
  post.content = mistune.markdown(request.form["content"]),
  session.add(post)
  session.commit()
  return redirect(url_for("posts"))


@app.route("/post/<int:id>/delete", methods=["GET"])
def delete_post_get(id):
  post = session.query(Post).get(id)
  return render_template("delete_post.html", post=post)

  
@app.route("/post/<int:id>/delete", methods=["POST"])
def delete_post_post(id):
  post = session.query(Post).get(id)
  session.delete(post)
  session.commit()
  return redirect(url_for("posts"))

@app.route("/login", methods=["GET"])
def login_get():
  return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
  email = request.form["email"]
  password = request.form["password"]
  user = session.query(User).filter_by(email=email).first()
  if not user or not check_password_hash(user.password, password):
    flash("Incorrect username or password", "danger")
    return redirect(url_for("login_get"))
  
  login_user(user)
  return redirect(request.args.get('next') or url_for("posts"))