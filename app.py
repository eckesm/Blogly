"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, DEFAULT_IMAGE_URL

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret_key_12345"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# -------------------------------------------------------------------


def get_list_users():
    return db.session.query(User.id, User.first_name, User.last_name).order_by(User.last_name, User.first_name).limit(25).all()

# -------------------------------------------------------------------


@app.route('/')
def show_home_page():
    """Show home page and users."""

    all_users = get_list_users()
    session['users'] = all_users

    return redirect('/home')


@app.route('/users')
def show_list_of_users():
    """Show home page and users."""

    all_users = get_list_users()
    session['users'] = all_users

    return redirect('/home')

#####################################################################
# ------------------------------ Users -----------------------------#
#####################################################################


@app.route('/home')
def show_users():
    """Show list of all users."""

    all_users = get_list_users()
    session['users'] = all_users

    users = User.query.order_by(User.last_name, User.first_name)
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    # order_by('created_at')

    return render_template('home.html', users=users, posts=posts)

# -------------------------------------------------------------------


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user."""
    user = User.query.get_or_404(user_id)
    posts = user.posts

    return render_template('details.html', user=user, posts=posts)

# -------------------------------------------------------------------


@app.route('/users/new')
def show_new_user_form():
    """Show new user form."""
    return render_template('new_user_form.html')

# -------------------------------------------------------------------


@app.route('/users/new', methods=['POST'])
def add_new_user_from_form():
    """Add new user to blogly_db."""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )

    db.session.add(new_user)
    db.session.commit()

    all_users = get_list_users()
    session['users'] = all_users

    flash(f"{new_user.full_name}'s profile has been created.", 'alert-info')

    return redirect('/home')

# -------------------------------------------------------------------


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show edit user form."""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user_form.html', user=user)

# -------------------------------------------------------------------


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Update user information in blogly_db."""

    edit_user = User.query.get_or_404(user_id)

    edit_user.first_name = request.form['first_name']
    edit_user.last_name = request.form['last_name']

    image_url = request.form['image_url']
    if image_url == '':
        edit_user.image_url = DEFAULT_IMAGE_URL

    db.session.add(edit_user)
    db.session.commit()

    all_users = get_list_users()
    session['users'] = all_users

    flash(f"{edit_user.full_name}'s profile has been updated.", 'alert-info')

    return redirect(f"/users/{user_id}")

# -------------------------------------------------------------------


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete user information from blogly_db."""

    user = User.query.get_or_404(user_id)
    full_name = user.full_name

    db.session.delete(user)
    db.session.commit()

    all_users = get_list_users()
    session['users'] = all_users

    flash(f"{full_name}'s profile has been deleted.", 'alert-info')

    return redirect('/home')

#####################################################################
# ------------------------------ Posts -----------------------------#
#####################################################################


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show specific post."""

    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template('single_post.html', post=post, user=user)

# -------------------------------------------------------------------


@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Show new post form for a given user."""

    user = User.query.get_or_404(user_id)
    return render_template('add_post_form.html', user=user)

# -------------------------------------------------------------------


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post_to_db(user_id):
    """Adds a new post from form to blogly_db."""

    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, owner_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    flash(
        f"{title} has been added to {user.full_name}'s profile", 'alert-info')

    return redirect(f"/users/{user_id}")

# -------------------------------------------------------------------


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show form to edit a post."""

    edit_post = Post.query.get_or_404(post_id)
    user = edit_post.user

    return render_template('edit_post_form.html', post=edit_post, user=user)

# -------------------------------------------------------------------


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post_in_database(post_id):
    """Edits selected post in blogly_db."""

    title = request.form['title']
    content = request.form['content']

    edit_post = Post.query.get_or_404(post_id)
    edit_post.title = title
    edit_post.content = content

    db.session.add(edit_post)
    db.session.commit()

    flash(
        f"{user.full_name}'s post entitled {title} has been edited.", 'alert-info')

    return redirect(f'/posts/{post_id}')

# -------------------------------------------------------------------


@app.route('/posts/<int:post_id>/delete')
def delete_post_from_database(post_id):
    """Deletes selected post from blogly_db."""

    post = Post.query.get_or_404(post_id)
    title = post.title
    user = post.user

    db.session.delete(post)
    db.session.commit()

    flash(
        f"{user.full_name}'s post entitled {title} has been deleted.", 'alert-info')

    return redirect(f'/users/{user.id}')
