import os

# To contain the configuration variables which control the Flask app.
# SQLALCHEMY_DATABASE_URI to set location of database, 
# DEBUG mode to help track down any errors in application,
# and SECRET_KEY to secure application.
  
class DevelopmentConfig(object):
  SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/blogful"
  DEBUG = True
  SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "PETER_PARKER_IS_SPIDERMAN")

class TestingConfig(object):
  SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/blogful-test"
  DEBUG = False
  SECRET_KEY = "Not secret"

class TravisConfig(object):
  SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/blogful-test"
  DEBUG = False
  SECRET_KEY = "Not secret"