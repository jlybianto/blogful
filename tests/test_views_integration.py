# Integration Testing
# Runs a little less quickly and gives information about how different elements are working together

import os
import unittest
from urlparse import urlparse

from werkzeug.security import generate_password_hash

# Configure your app to use the testing configuration
if not "CONFIG_PATH" in os.environ:
  os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
  def setUp(self):
    """
    Test setup
    """
    self.client = app.test_client()
    
    # Set up the tables in the database
    Base.metadata.create_all(engine)
    
    # Create an example user
    self.user = models.User(name="Alice", email="alice@example.com",
                            password=generate_password_hash("test"))
    session.add(self.user)
    session.commit()

  def tearDown(self):
    """
    Test teardown
    """
    session.close()
    # Remove the tables and their data from the database
    Base.metadata.drop_all(engine)
  
  def simulate_login(self):
    # Mimics what Flask-Login looks for when determining whether a user is logged in
    with self.client.session_transaction() as http_session:
      http_session["user_id"] = str(self.user.id)
      http_session["_fresh"] = True
  
  def testAddPost(self):
    # To act as a logged in user
    self.simulate_login()
    
    # Send a POST request
    response = self.client.post("/post/add", data={
        "title": "Test Post",
        "content": "Test Content"
        })
    
    self.assertEqual(response.status_code, 302)
    self.assertEqual(urlparse(response.location).path, "/")
    posts = session.query(models.Post).all()
    self.assertEqual(len(posts), 1)
    
    post = posts[0]
    self.assertEqual(post.title, "Test Post")
    self.assertEqual(post.content, "<p>Test Content</p>\n")
    self.assertEqual(post.author, self.user)
    
  def testEditPost(self):
    # To act as a logged in user
    self.simulate_login()
    
    # Send a POST request to add
    response = self.client.post("/post/add", data={
        "title": "Test Post",
        "content": "Test Content"
        })
    
    self.assertEqual(response.status_code, 302)
    self.assertEqual(urlparse(response.location).path, "/")
    posts = session.query(models.Post).all()
    self.assertEqual(len(posts), 1)    
    
    # Send a POST request to edit
    post = posts[0].id
    self.client.post("/post/{}/edit".format(post), data={
        "title": "Change Test Post",
        "content": "Change Test Content"
      })
    
    post = session.query(models.Post).first()    
    self.assertEqual(post.title, "Change Test Post")
    self.assertEqual(post.content, "<p>Change Test Content</p>\n")
    self.assertEqual(post.author, self.user)
    
  def testDeletePost(self):
    # To act as a logged in user
    self.simulate_login()
    
    # Send a POST request to add
    response = self.client.post("/post/add", data={
        "title": "Test Post",
        "content": "Test Content"
        })
    
    self.assertEqual(response.status_code, 302)
    self.assertEqual(urlparse(response.location).path, "/")
    posts = session.query(models.Post).all()
    self.assertEqual(len(posts), 1)
    
    # Send a POST request to delete
    post = posts[0].id
    self.client.post("/post/{}/delete".format(post))
    posts = session.query(models.Post).all()
    self.assertEqual(len(posts), 0)

# Run tests using 'PYTHONPATH=. python tests/test_views_integration.py'
# Set PYTHONPATH environment variable to import the blog module
# Even though it is in a different location to the test files
if __name__ == "__main__":
  unittest.main()