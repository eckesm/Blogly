"""Seed file to make sample data for blogly db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
# User.query.delete()

# Seed users
user1 = User(first_name='Bradley', last_name='Cooper',
             image_url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.caa.com%2Fsites%2Fdefault%2Ffiles%2Fspeaker-headshots%2FCooperB_headshot_web-1.jpg&f=1&nofb=1')
user2 = User(first_name='Dolly', last_name='Parton',
             image_url='https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fmediad.publicbroadcasting.net%2Fp%2Fwvxu%2Ffiles%2Fstyles%2Fx_large%2Fpublic%2F201612%2Fdolly_parton_headshot_nbc_dec_2016.jpg&f=1&nofb=1')
user3 = User(first_name='Dana', last_name='Scully',
             image_url='https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fimages.hellogiggles.com%2Fuploads%2F2016%2F10%2F10061623%2Fscully2.jpg&f=1&nofb=1')
user4 = User(first_name='Taylor', last_name='Swift',
             image_url='https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fthefappeningblog.com%2Fwp-content%2Fuploads%2F2018%2F05%2FTaylor-Swift-Sexy-TheFappeningBlog.com-170.jpg&f=1&nofb=1')
user5 = User(first_name='Lady', last_name='Gaga',
             image_url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.cheatsheet.com%2Fwp-content%2Fuploads%2F2021%2F02%2FLady-Gaga-5-1024x683.jpg%3Fx88813&f=1&nofb=1')
user6 = User(first_name='Joe', last_name='Biden')

# Seed posts
post1 = Post(title='Working 9 to 5',
             content='The boss man must perish so we working gals can make ends meet!', owner_id=2)
post2 = Post(title='Jolene and her flaws',
             content="Too many to list in one post, but let's just say she's not chaste. ", owner_id=2)
post3 = Post(title="I'm a medical doctor.",
             content="So it can be hard for me to be with Mulder all the time because he does not follow the rules!", owner_id=3)
post4 = Post(title="How to tell if you are an alien",
             content="Well, you may not be an alien, but that doesn't mean that you aren't being abducted.", owner_id=3)
post5 = Post(title="What it's like being Bradley Cooper",
             content="It's pretty awesome, tbh.", owner_id=1)
post6 = Post(title="Owning an Amusement Park",
             content="Y'all should come down to Tennessee and check out Dollywood!  We've got a rodeo and everything!", owner_id=2)
post7 = Post(title="Life in a Fairytale",
             content="Well, breakups are hard... but being filthy rich isn't.", owner_id=4)
post8 = Post(title="Woman of the Decade Speech",
             content="Lorem, ipsum dolor sit amet consectetur adipisicing elit. Repudiandae ducimus distinctio, consequuntur nesciunt sint odit minus incidunt suscipit autem accusamus, eligendi quis fugiat quod necessitatibus culpa neque, repellendus commodi mollitia.Lorem, ipsum dolor sit amet consectetur adipisicing elit. Repudiandae ducimus distinctio, consequuntur nesciunt sint odit minus incidunt suscipit autem accusamus, eligendi quis fugiat quod necessitatibus culpa neque, repellendus commodi mollitia.Lorem, ipsum dolor sit amet consectetur adipisicing elit. Repudiandae ducimus distinctio, consequuntur nesciunt sint odit minus incidunt suscipit autem accusamus, eligendi quis fugiat quod necessitatibus culpa neque, repellendus commodi mollitia.Lorem, ipsum dolor sit amet consectetur adipisicing elit. Repudiandae ducimus distinctio, consequuntur nesciunt sint odit minus incidunt suscipit autem accusamus, eligendi quis fugiat quod necessitatibus culpa neque, repellendus commodi mollitia.Lorem, ipsum dolor sit amet consectetur adipisicing elit. Repudiandae ducimus distinctio, consequuntur nesciunt sint odit minus incidunt suscipit autem accusamus, eligendi quis fugiat quod necessitatibus culpa neque, repellendus commodi mollitia.Lorem, ipsum dolor sit amet consectetur adipisicing elit. Repudiandae ducimus distinctio, consequuntur nesciunt sint odit minus incidunt suscipit autem accusamus, eligendi quis fugiat quod necessitatibus culpa neque, repellendus commodi mollitia.Lorem, ipsum dolor sit amet consectetur adipisicing elit. Repudiandae ducimus distinctio, consequuntur nesciunt sint odit minus incidunt suscipit autem accusamus, eligendi quis fugiat quod necessitatibus culpa neque, repellendus commodi mollitia.Lorem, ipsum dolor sit amet consectetur adipisicing elit. Repudiandae ducimus distinctio, consequuntur nesciunt sint odit minus incidunt suscipit autem accusamus, eligendi quis fugiat quod necessitatibus culpa neque, repellendus commodi mollitia.", owner_id=4)

db.session.add_all([user1, user2, user3, user4, user5, user6])
db.session.commit()

db.session.add_all([post8, post1, post2, post3, post4, post5, post6, post7])
db.session.commit()
