"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret_key_12345"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def show_home_page():
    """Show home page."""
    return redirect('/users')


@app.route('/users')
def show_users():
    """Show list of all users."""
    # users = User.query.all()
    users = User.query.order_by(User.last_name, User.first_name)
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user."""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)


@app.route('/users/new')
def show_new_user_form():
    """Show new user form."""
    return render_template('new_user_form.html')


@app.route('/users/new', methods=['POST'])
def add_new_user_from_form():
    """Add new user to users table from New User form."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    if image_url == '':
        new_user = User(first_name=first_name, last_name=last_name)
    else:
        new_user = User(first_name=first_name,
                        last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    # return redirect(f"/users/{new_user.id}")
    return redirect('/users')


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show edit user form."""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user_form.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Update user information."""

    edit_user = User.query.get_or_404(user_id)

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    edit_user.first_name = first_name
    edit_user.last_name = last_name

    delattr(edit_user, 'image_url')
    if image_url == '':
        edit_user.image_url = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fpce-coops.com%2Fwp-content%2Fuploads%2F2019%2F04%2Fblank-profile-picture-973460_1280-e1561474127956.png&f=1&nofb=1'
    else:
        edit_user.image_url = image_url

    db.session.add(edit_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete user information."""

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')
