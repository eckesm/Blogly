from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

# python -m unittest test_models.py

class UserModelTestCase(TestCase):
    """Tests for User class."""

    def setUp(self):
        """Clean up any existing users."""
        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_get_full_name(self):
        """Test get_full_name method."""
        user = User(first_name="TestFirst", last_name="TestLast")
        self.assertEquals(user.full_name, "TestFirst TestLast")