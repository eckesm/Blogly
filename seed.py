"""Seed file to make sample data for blogly db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
user1 = User(first_name='Bradley', last_name='Cooper', image_url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.caa.com%2Fsites%2Fdefault%2Ffiles%2Fspeaker-headshots%2FCooperB_headshot_web-1.jpg&f=1&nofb=1')
user2 = User(first_name='Dolly', last_name='Parton', image_url='https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fmediad.publicbroadcasting.net%2Fp%2Fwvxu%2Ffiles%2Fstyles%2Fx_large%2Fpublic%2F201612%2Fdolly_parton_headshot_nbc_dec_2016.jpg&f=1&nofb=1')
user3 = User(first_name='Dana', last_name='Scully', image_url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.viUX4xsi-XXO8aVp5XdYYwHaLA%26pid%3DApi&f=1')

# Add new objects to session, so they'll persist
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# Commit--otherwise, this never gets saved!
db.session.commit()
