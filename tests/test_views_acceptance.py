# Acceptance Testing
# Runs slower but gives information about the whole system

import os
import unittest

# Module in order to start the Flask test server
# Gives the ability to start and run other code simultaneously with scripts
# Control by calling 'start' and 'terminate' methods
import multiprocessing

import time
from urlparse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

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
    self.browser = Browser("phantomjs")
    
    # Set up the tables in the database
    Base.metadata.create_all(engine)
    
    # Create an example user
    self.user = models.User(name="Alice", email="alice@example.com",
                           password=generate_password_hash("test"))
    session.add(self.user)
    session.commit()
    
    self.process = multiprocessing.Process(target=app.run)
    self.process.start()
    time.sleep(1)

  def tearDown(self):
    """
    Test teardown
    """
    # Remove the tables and their data from the database
    self.process.terminate()
    session.close()
    engine.dispose()
    Base.metadata.drop_all(engine)
    self.browser.quit()
    
  def testLoginCorrect(self):
    self.browser.visit("http://0.0.0.0:5000/login")
    self.browser.fill("email", "alice@example.com")
    self.browser.fill("password", "test")
    button = self.browser.find_by_css("button[type=submit]")
    button.click()
    self.assertEqual(self.browser.url, "http://0.0.0.0:5000/")
  
  def testLoginIncorrect(self):
    self.browser.visit("http://0.0.0.0:5000/login")
    self.browser.fill("email", "bob@example.com")
    self.browser.fill("password", "test")
    button = self.browser.find_by_css("button[type=submit]")
    button.click()
    self.assertEqual(self.browser.url, "http://0.0.0.0:5000/login")

# Run tests using 'PYTHONPATH=. python tests/test_views_acceptance.py'
# Set PYTHONPATH environment variable to import the blog module
# Even though it is in a different location to the test files
if __name__ == "__main__":
  unittest.main()