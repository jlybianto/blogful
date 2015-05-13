import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from .database import Base, engine

from flask.ext.login import UserMixin

# Update models to have a One-to-Many relationship between User and Post
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base, UserMixin):
  """
  Inherits from the declarative base and Flask-Login UserMixin class which adds a series of default methods to make authentication work.
  """
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True)
  name = Column(String(128))
  email = Column(String(128), unique=True)
  password = Column(String(128))
  # Add One-to-Many relationship between the User and Post model
  posts = relationship("Post", backref="author")

class Post(Base):
  __tablename__ = "posts"
  
  id = Column(Integer, primary_key=True)
  title = Column(String(1024))
  content = Column(Text)
  datetime = Column(DateTime, default=datetime.datetime.now)
  # Add One-to-Many relationship between the User and Post model
  author_id = Column(Integer, ForeignKey('users.id'))

Base.metadata.create_all(engine)