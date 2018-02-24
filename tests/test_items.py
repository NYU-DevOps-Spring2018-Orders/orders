"""
Test cases for Item Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from models.item import Item, DataValidationError
from app import app, db

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestItems(unittest.TestCase):
    """ Test Cases for Items """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_an_item(self):
        """ Create a item and assert that it exists """
        item = Item(product_id=1, name="wrench", quantity=1, price=10.50)
        self.assertTrue(item != None)
        self.assertEqual(item.id, None)
        self.assertEqual(item.product_id, 1)
        self.assertEqual(item.name, "wrench")
        self.assertEqual(item.quantity, 1)
        self.assertEqual(item.price, 10.50)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
