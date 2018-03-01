"""
Orders API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""

import unittest
import os
import json
import logging
from datetime import datetime
from flask_api import status    # HTTP Status Codes
from mock import MagicMock, patch

from models import Item, Order, DataValidationError, db
import server

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestServer(unittest.TestCase):
    """ Orders Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        server.app.debug = False
        server.initialize_logging(logging.INFO)
        # Set up the test database
        server.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        server.init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        date = datetime.now()

        Item(product_id=1, name='hammer', quantity=1, price=11.50).save()
        Item(product_id=2, name='toilet paper', quantity=2, price=2.50).save()
        order = Order(customer_id=1, date=date, shipped=True).save()
        order = Order(customer_id=2, date=date, shipped=True).save()
        self.app = server.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'success')

    def test_get_item_list(self):
        """ Get a list of Items """
        resp = self.app.get('/items')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_order_list(self):
        """ Get a list of Orders """
        resp = self.app.get('/orders')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_item_not_found(self):
        """ Get an item thats not found """
        resp = self.app.get('/items/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_order_not_found(self):
        """ Get an order thats not found """
        resp = self.app.get('/orders/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


######################################################################
# Utility functions
######################################################################

    def get_item_count(self):
        """ save the current number of items """
        resp = self.app.get('/items')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)

    def get_order_count(self):
        """ save the current number of orders """
        resp = self.app.get('/orders')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
