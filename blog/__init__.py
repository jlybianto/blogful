import os

# Import the Flask object and create the app
from flask import Flask

app = Flask(__name__)

# Use config_path to switch between configurations easily in different situations
config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig")
app.config.from_object(config_path)

# Import Views and Jinja filters after app creation because both make use of app object
from . import views
from . import filters

# Import Login system
from . import login