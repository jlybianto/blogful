from flask.ext.login import LoginManager

from blog import app
from .database import session
from .models import User

# Create and initializes LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Redirect unauthorized users when trying to access a protected resource
login_manager.login_view = "login_get"
# Classify error messages from Flask-Login in conjunction with Bootstrap's alert system
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(id):
  return session.query(User).get(int(id))