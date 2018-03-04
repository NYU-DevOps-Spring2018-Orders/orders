"""
Test cases for Order Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from datetime import datetime

from models import Order, DataValidationError, db
from werkzeug.exceptions import NotFound
from server import app

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestOrders(unittest.TestCase):
    """ Test Cases for Orders """

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
        Order.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_an_order(self):
        """ Create an order and assert that it exists """
        date = datetime.now()
        order = Order(customer_id=1, date=date, shipped=True)

        self.assertEqual(order.id, None)
        self.assertEqual(order.customer_id, 1)
        self.assertEqual(order.date, date)
        self.assertEqual(order.shipped, True)

    def test_add_an_order(self):
        """ Create an Order and add it to the database """
        date = datetime.now()
        orders = Order.all()
        self.assertEqual(orders, [])
        order = Order(customer_id=1, date=date, shipped=True)
        self.assertEqual(order.id, None)
        order.save()

        self.assertEqual(order.id, 1)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

    def test_update_an_order(self):
        """ Update an Order """
        date = datetime.now()
        order = Order(customer_id=1, date=date, shipped=True)
        order.save()
        self.assertEqual(order.id, 1)

        order.shipped = False
        order.save()

        orders = Order.all()
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].shipped, False)

    def test_delete_an_order(self):
        """ Delete an Order """
        date = datetime.now()
        order = Order(customer_id=1, date=date, shipped=True)
        order.save()
        self.assertEqual(len(Order.all()), 1)

        order.delete()
        self.assertEqual(len(Order.all()), 0)

    def test_serialize_an_order(self):
        """ Test serialization of an Order """
        date = datetime.now()
        order = Order(customer_id=1, date=date, shipped=True)
        data = order.serialize()

        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], None)

        self.assertIn('customer_id', data)
        self.assertEqual(data['customer_id'], 1)
        self.assertIn('date', data)
        self.assertEqual(data['date'], date)
        self.assertIn('shipped', data)
        self.assertEqual(data['shipped'], True)

    def test_deserialize_an_order(self):
        """ Test deserialization of an Order """
        date = str(datetime.now())
        data = {"id": 1, "customer_id": 1, "date": date, "shipped": 1}
        order = Order()
        order.deserialize(data)

        self.assertNotEqual(order, None)
        self.assertEqual(order.id, None)
        self.assertEqual(order.customer_id, 1)
        self.assertEqual(str(order.date), date)
        self.assertEqual(order.shipped, True)

    def test_fetch_all_orders(self):
        """ Test fetching all Orders """
        date = datetime.now()
        order = Order(customer_id=1, date=date, shipped=True)
        order.save()
        order2 = Order(customer_id=2, date=date, shipped=False)
        order2.save()
        Order.all()

        self.assertEqual(len(Order.all()), 2)

    def test_get_an_order(self):
        """ Get an Order by id """
        date = datetime.now()
        order = Order(customer_id=1, date=date, shipped=True)
        order.save()

        order1 = Order.get(order.id)

        self.assertEqual(order.id, order1.id)
        self.assertEqual(order1.date, date)

    def test_get_or_404(self):
        """ Get_or_404 function with nonexistent ID """
        self.assertRaises(NotFound, Order.get_or_404, 1)

    def test_find_by_customer_id(self):
        """ Find orders by customer_id """
        date = datetime.now()
        order = Order(customer_id=1, date=date, shipped=True)
        order.save()
        order1 = Order.find_by_customer_id(order.customer_id)
        self.assertEqual(order1[0].customer_id, order.customer_id)
        self.assertEqual(order1[0].date, date)

    def test_find_by_date(self):
        """ Find orders by date """
        date = datetime.now()
        order = Order(customer_id=1, date=date, shipped=True)
        order.save()
        order1 = Order(customer_id=2, date=date, shipped=False)
        order1.save()
        order2 = Order.find_by_date(date)
        self.assertEqual(order2[0].customer_id, order.customer_id)
        self.assertEqual(order2[0].shipped, order.shipped)
        self.assertEqual(order2[0].date, order.date)

    def test_find_by_shipped(self):
        """ Find orders by shipped """
        date = datetime.now()
        order = Order(customer_id=1, date=date, shipped=True)
        order.save()
        order1 = Order(customer_id=2, date=date, shipped=False)
        order1.save()
        order2 = Order.find_by_shipped(True)
        self.assertEqual(order2[0].customer_id, order.customer_id)
        self.assertEqual(order2[0].shipped, order.shipped)
        self.assertEqual(order2[0].date, order.date)

    def test_non_dict_raises_error(self):
        """ Pass invalid data structure deserialize """
        data = [1,2,3]
        order = Order()

        with self.assertRaises(DataValidationError):
            order.deserialize(data)

    def test_invalid_key_raises_error(self):
        """ Try to pass invalid key """
        date = datetime.now()
        data = {"id": 1, "date": date, "shipped": 1}

        with self.assertRaises(DataValidationError):
            order = Order()
            order.deserialize(data)

    def test_repr(self):
        """ Test that string representation is correct """
        date = datetime.now()
        order = Order(customer_id=1, date=date, shipped=True)
        order.save()

        self.assertEqual(order.__repr__(), "<Order>")
        
    def test_cancel_an_order(self):
        """ Cancel an Order """
        date = datetime.now()
        order = Order(customer_id=2, date=date, shipped = False)
        order.save()
        self.assertEqual(len(Order.all()), 1)

        order.delete()
        self.assertEqual(len(Order.all()), 0)    
        

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
