"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


DEFAULT_IMAGE_URL = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fpce-coops.com%2Fwp-content%2Fuploads%2F2019%2F04%2Fblank-profile-picture-973460_1280-e1561474127956.png&f=1&nofb=1'


class User(db.Model):
    """User model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text, nullable=False,
                          default=DEFAULT_IMAGE_URL)

    posts = db.relationship(
        'Post', backref='user', cascade='all, delete-orphan')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @full_name.setter
    def full_name(self, name):
        first_name, last_name = name.split()
        self.first_name = first_name
        self.last_name = last_name

    @full_name.deleter
    def full_name(self):
        self.first_name = None
        self.last_name = None

    def __repr__(Self):
        u = Self
        return f"<User id={u.id} name={u.full_name}>"


class Post(db.Model):
    """Post model."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=func.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    posts_tags = db.relationship(
        'PostTag', backref='post', cascade='all, delete-orphan')

    tags = db.relationship('Tag', secondary='posts_tags', backref='posts')

    def __repr__(Self):
        p = Self
        return f"<Post id={p.id} title={p.title} owner={p.user.full_name}>"




class Tag(db.Model):
    """Tag model."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False, unique=True)

    posts_tags = db.relationship(
        'PostTag', backref='tag', cascade='all, delete-orphan')


class PostTag(db.Model):
    """PostTag model."""

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
