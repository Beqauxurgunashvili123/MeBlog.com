from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, login_required, current_user
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename, os
from ext import app, db
from forms import Post, RegisterForm, LoginForm
from models import Article, User


@app.route("/")
def index():
    articles = Article.query.order_by(desc(Article.timestamp)).all()
    return render_template('index.html', articles=articles)

@app.route("/add_article", methods=["POST", "GET"])
@login_required
def add_article():

    form = Post()

    if form.validate_on_submit():
        try:
            if form.img.data:
                f = form.img.data
                filename = secure_filename(f.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                f.save(save_path)
                img_filename = filename
            else:
                img_filename = None

            new_article = Article(
                title=form.title.data,
                content=form.content.data,
                img=img_filename,
                user_id=current_user.id
            )
            db.session.add(new_article)
            db.session.commit()


            flash("Article added successfully", "success")
        finally:
            return redirect(url_for('index'))


    return render_template('add_article.html', form=form)


@app.route("/update_article/<int:product_id>", methods=["POST"])
@login_required
def update_article(product_id):
    chosen_post = Article.query.get(product_id)
    if not chosen_post:
        return render_template("404.html")

    if current_user != chosen_post.author:
        abort(403)

    form = Post(title=chosen_post, content=chosen_post.content)
    if form.validate():
        chosen_post.title = form.title.data
        chosen_post.content = form.content.data

        if form.img.data:
            old_img_path = os.path.join(app.config['UPLOAD_FOLDER'], chosen_post.img)
            if os.path.exists(old_img_path):
                os.remove(old_img_path)

            f = form.img.data
            filename = secure_filename(f.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(save_path)
            chosen_post.img = filename

        db.session.commit()

        flash("Post updated successfully", "success")
        return redirect(url_for('index'))
    else:
        flash("Error updating Post", "danger")

    return render_template("edit_article.html", form=form, chosen_post=chosen_post)


@app.route("/edit_article/<int:product_id>", methods=["POST", "GET"])
@login_required
def edit_article(product_id):
    chosen_post = Article.query.get(product_id)


    if current_user != chosen_post.author:
        abort(403)
    form = Post(title=chosen_post.title, content=chosen_post.content)
    return render_template("edit_article.html", form=form, chosen_post=chosen_post)



@app.route("/delete_article/<int:product_id>", methods=["POST"])
@login_required
def delete_article(product_id):
    article = Article.query.get(product_id)


    if current_user != article.author:
        abort(403)


    if article:
        db.session.delete(article)
        db.session.commit()
        flash('Article deleted successfully', 'success')
    else:
        flash('Article not found', 'danger')

    return redirect(url_for('index'))




@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')

        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("index"))

    return render_template("login.html", form=form)




@app.route("/about")
def about():
    soft = "flask"
    lang = "Python"
    return render_template('about.html', soft=soft, proglang=lang)
@app.route("/sponsorlink")
def sponsor():
    return render_template("sponsorlink.html")
@app.route("/tutorial")
def howto():
    return render_template("tutorial.html")
@app.route("/success")
def success():
    return render_template('success.html')
@app.route("/search_results", methods=["POST", "GET"])
def search():
    query = request.form.get("query")

    if query:
        results = Article.query.filter(Article.title.ilike(f"%{query}%")).all()
    else:
        results = []
    return render_template("search_results.html",  results=results, query=query)