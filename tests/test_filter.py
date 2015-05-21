# Unit Testing
# Runs very quickly but only gives information about isolated sections of the code

import os
import unittest
import datetime

# Configure your app to use the testing configuration
if not "CONFIG_PATH" in os.environ:
  os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

import blog
from blog.filters import *

class FilterTests(unittest.TestCase):
  def testDateFormat(self):
    # Tonight we're gonna party...
    # First test creates a datetime.date object, runs through the dateformat function
    # Makes sure that the resulting string is correct
    date = datetime.date(1999, 12, 31)
    formatted = dateformat(date, "%y/%m/%d")
    self.assertEqual(formatted, "99/12/31")
  
  def testDateFormatNone(self):
    # Second test passes 'None' into the dateformat function
    # Makes sure that a 'None' object is returned
    formatted = dateformat(None, "%y/%m/%d")
    self.assertEqual(formatted, None)

# Run tests using 'PYTHONPATH=. python tests/test_filter.py'
# Set PYTHONPATH environment variable to import the blog module
# Even though it is in a different location to the test files
if __name__ == "__main__":
  unittest.main()