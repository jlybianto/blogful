# Import Manager object and create an instance
import os
from flask.ext.script import Manager
from blog import app

manager = Manager(app)

@manager.command
def run():
  # Attempt to retrieve a port number from environment - 8080 if unavailable
  # Number of hosts use the PORT environment variable to tell the app
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)


# To display post entries
from blog.models import Post
from blog.database import session

@manager.command
# Add a series of dummy posts for the post content to be tested
def seed():
  content = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
  
  for i in range(25):
    post = Post(title="Test Post #{}".format(i), content=content)
    session.add(post)
  session.commit()


# For users and authentication security
from getpass import getpass
from werkzeug.security import generate_password_hash
from blog.models import User

@manager.command
# To add new users
# Request name, e-mail address and password twice for verification
def adduser():
  name = raw_input("Name: ")
  email = raw_input("E-mail: ")
  if session.query(User).filter_by(email=email).first():
    print "User with that e-mail address already exists"
    return
  
  password = ""
  password_2 = ""
  while not (password and password_2) or password != password_2:
    password = getpass("Password: ")
    password_2 = getpass("Re-enter password: ")
  # Hashing converts plain text password into string of characters
  # Utilize one-way hash to obtain characters from text but not vice versa
  user = User(name=name, email=email, password=generate_password_hash(password))
  session.add(user)
  session.commit()


# Manage database migrations using Flask-Migrate
# Migrations allow setting up a series of scripts
# To easily move between different database schemas, add/removing columns
# SQLAlchemy has a migration tool called Alembic
from flask.ext.migrate import Migrate, MigrateCommand
from blog.database import Base

class DB(object):
  """
  Designed to hold metadata object. Alembic uses the metadata to work out what the changes to the database schema should be.
  """
  def __init__(self, metadata):
    self.metadata = metadata

# Create an instance of the Flask-Migrate class
# Add all of the commands held in the Migrate class to the management script
# Run 'python manage.py db migrate' to generate a migration script
# If script looks correct then 'python manage.py db upgrade' will apply the changes
# To roll back changes, run 'python manage.py downgrade' to reverse migration
migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)


# Call the run function by "python manage.py run"
if __name__ == "__main__":
  manager.run()