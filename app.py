"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag, DEFAULT_IMAGE_URL

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


def get_list_tags():
    return db.session.query(Tag.id, Tag.name).order_by(Tag.name).limit(25).all()

# -------------------------------------------------------------------


@app.route('/')
def show_home_page():
    """Show home page, users, and tags."""
    return redirect('/home')


@app.route('/users')
def show_list_of_users():
    """Show home page, users, and tags."""
    return redirect('/home')


@app.route('/tags')
def show_list_of_tags():
    """Show home page, users, and tags."""
    return redirect('/home')

#####################################################################
# ------------------------------ Users -----------------------------#
#####################################################################


@app.route('/home')
def show_users():
    """Show list of all users."""

    session['users'] = get_list_users()
    session['tags'] = get_list_tags()

    users = User.query.order_by(User.last_name, User.first_name)
    tags = Tag.query.order_by(Tag.name)
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template('home.html', users=users, tags=tags, posts=posts)

# -------------------------------------------------------------------


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user."""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(owner_id=user_id).order_by(
        Post.created_at.desc()).all()

    return render_template('details.html', user=user, posts=posts)

# -------------------------------------------------------------------


@app.route('/users/new')
def show_new_user_form():
    """Show new user form."""
    return render_template('add_user_form.html')

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

    session['users'] = get_list_users()

    flash(f"{new_user.full_name}'s profile has been created.", 'alert-info')

    return redirect(f'/users/{new_user.id}')

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

    session['users'] = get_list_users()

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

    session['users'] = get_list_users()

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
    tags = Tag.query.order_by(Tag.name)

    return render_template('add_post_form.html', user=user, tags=tags)

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

    flash(f"{title} has been added to {user.full_name}'s profile", 'alert-info')

    # tags = Tag.query.order_by(Tag.name)
    # for tag in tags:
    #     if request.form.get(f'tag-{tag.id}') == 'on':
    #         new_post.tags.append(tag)

    checked_tags = request.form.getlist('tag_checkbox')
    tags = Tag.query.order_by(Tag.name)
    for tag in tags:
        if str(tag.id) in checked_tags:
            new_post.tags.append(tag)
    
    db.session.commit()

    return redirect(f"/users/{user_id}")

# -------------------------------------------------------------------


@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def show_edit_post_form(post_id):
    """Show form to edit a post."""

    edit_post = Post.query.get_or_404(post_id)
    user = edit_post.user
    tags = Tag.query.order_by(Tag.name)

    tags_status_list = []

    for tag in tags:
        if tag in edit_post.tags:
            tags_status_list.append(tuple((tag, True)))
        else:
            tags_status_list.append(tuple((tag, False)))

    return render_template('edit_post_form.html', post=edit_post, user=user, tags=tags_status_list)

# -------------------------------------------------------------------


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post_in_database(post_id):
    """Edits selected post in blogly_db."""

    title = request.form['title']
    content = request.form['content']

    edit_post = Post.query.get_or_404(post_id)
    edit_post.title = title
    edit_post.content = content

    checked_tags = request.form.getlist('tag_checkbox')
    tags = Tag.query.order_by(Tag.name)
    for tag in tags:
        if str(tag.id) in checked_tags:
            edit_post.tags.append(tag)
        else:
            pt_to_delete = PostTag.query.filter_by(
                post_id=edit_post.id, tag_id=tag.id).one_or_none()
            if pt_to_delete != None:
                db.session.delete(pt_to_delete)

    db.session.add(edit_post)
    db.session.commit()

    flash(
        f"{edit_post.user.full_name}'s post entitled {title} has been edited.", 'alert-info')

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


#####################################################################
# ------------------------------- Tags -----------------------------#
#####################################################################

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show posts for specific tag."""

    tag = Tag.query.get_or_404(tag_id)
    posts = db.session.query(Post).filter(PostTag.tag_id == tag_id).join(
        PostTag).order_by(Post.created_at.desc()).all()

    return render_template('tag.html', posts=posts, tag=tag)

# -------------------------------------------------------------------


@app.route('/tags/new', methods=['GET'])
def show_add_tag_form():
    """Show add tag form."""

    return render_template('add_tag_form.html')

# -------------------------------------------------------------------


@app.route('/tags/new', methods=['POST'])
def add_tag():
    """Show add tag form."""

    name = request.form['name']
    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    session['tags'] = get_list_tags()

    flash(
        f"{name} tag has been created.", 'alert-info')

    return redirect(f'/tags/{new_tag.id}')

# -------------------------------------------------------------------


@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def show_edit_tag_form(tag_id):
    """Show edit tag form."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit_tag_form.html', tag=tag)

# -------------------------------------------------------------------


@app.route('/tags/<int:tag_id>/delete')
def delete_tag_from_database(tag_id):
    """Deletes selected post from blogly_db."""

    tag = Tag.query.get_or_404(tag_id)
    name = tag.name

    db.session.delete(tag)
    db.session.commit()

    flash(
        f"{name} tag has been deleted.", 'alert-info')

    return redirect('/tags')
