import os

class DevelopmentConfig(object):
  """
  To contain the configuration variables which control the Flask app. SQLALCHEMY_DATABASE_URI to set location of database, DEBUG mode to help track down any errors in application and SECRET_KEY to secure application.
  """
  SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/blogful"
  DEBUG = True
  SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "PETER_PARKER_IS_SPIDERMAN")