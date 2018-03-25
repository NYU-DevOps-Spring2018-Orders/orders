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

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_409_CONFLICT = 409
HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415
HTTP_500_INTERNAL_SERVER_ERROR = 500

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

        item = Item(order_id=1, product_id=1, name='hammer', quantity=1, price=11.50).save()
        item = Item(order_id=1, product_id=2, name='toilet paper', quantity=2, price=2.50).save()
        item = Item(order_id=2, product_id=3, name='beer', quantity=2, price=10.50).save()
        order = Order(customer_id=1, date=date, status = 'processing').save()
        order = Order(customer_id=2, date=date, status = 'processing').save()
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
        self.assertEqual(len(data), 3)

    def test_get_order_list(self):
        """ Get a list of Orders """
        resp = self.app.get('/orders')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_list_orders_by_status(self):
        """ Get list of orders by status """
        resp = self.app.get('/orders/query?status=processing')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_list_orders_by_customer_id(self):
        """ Get list of orders by customer id """
        resp = self.app.get('/orders/query?customer_id=1')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 1)

    def test_list_orders_by_no_field(self):
        """ Get all orders if no field is specified """
        resp = self.app.get('/orders/query')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_list_items_by_order_id(self):
        """ Get list of items by order id """
        resp = self.app.get('/items/query?order_id=1')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_list_items_by_prodcut_id(self):
        """ Get list of items by product id """
        resp = self.app.get('/items/query?product_id=1')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 1)

    def test_list_items_by_quantity(self):
        """ Get list of items by quantity """
        resp = self.app.get('/items/query?quantity=2')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_list_items_by_price(self):
        """ Get list of items by price """
        resp = self.app.get('/items/query?price=10.50')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 1)

    def test_list_items_by_name(self):
        """ Get list of items by name """
        resp = self.app.get('/items/query?name=beer')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 1)

    def test_list_items_by_no_field(self):
        """ Get all items if no field is specified """
        resp = self.app.get('/items/query')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 3)

    def test_get_order_item_list(self):
        """ Get a list of Items from an Order """
        order = Order.find_by_customer_id(1)[0]
        print order.id
        resp = self.app.get('/orders/{}/items'.format(order.id),
                            content_type='application/json')
        print json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_order(self):
        """ Get a single Order """
        # get the id of a order
        order = Order.find_by_customer_id(1)[0]
        resp = self.app.get('/orders/{}'.format(order.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['customer_id'], order.customer_id)

    def test_get_item(self):
        """ Get a single Item """
        # get the id of a item
        item = Item.find_by_name('hammer')[0]
        resp = self.app.get('/items/{}'.format(item.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['price'], 11.5)

    def test_get_order_not_found(self):
        """ Get an order thats not found """
        resp = self.app.get('/orders/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_item_not_found(self):
        """ Get an item thats not found """
        resp = self.app.get('/items/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_order(self):
        """ Create a new Order and items handling"""
        # save the current number of orders for later comparison
        order_count = self.get_order_count()
        item_count = self.get_item_count()
        # add a new order. order id is 3 since there are 2 orders initially
        new_order = {'customer_id': 1, 'date': "2018-03-01 18:55:36.985524", 'status': 'processing'}
        new_order['items'] = [{"order_id": 3, "product_id": 3, "name": "Rice", "quantity": 1, "price": "4.50"}]
        data = json.dumps(new_order)
        resp = self.app.post('/orders', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertTrue(location != None)

        """
        Check the data is correct by verifying that the customer_id and
        order_id are correct
        """
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['customer_id'], 1)
        self.assertEqual(new_json['items'][0]["order_id"], 3)
        self.assertEqual(len(new_json['items']), 1)
        """
        Check that response is correct for the order and that order count has
        increased to reflect new order
        """
        resp = self.app.get('/orders')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), order_count + 1)
        new_json_orders = new_json.copy()
        new_json_orders.pop('items')
        self.assertIn(new_json_orders, data)
        """
        Check that response is correct for the order's items and that
        item count has increased to reflect items in the new order
        """
        resp = self.app.get('/items')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), item_count + 1)
        new_json_items = new_json.pop('items')[0]
        self.assertIn(new_json_items, data)

    def test_create_wrong_content_type(self):
        """ Creating wrong content type """
        order_count = self.get_order_count()
        item_count = self.get_item_count()
        new_order = {'customer_id': 1, 'date': "2018-03-01 18:55:36.985524", 'status': 'processing'}
        new_order['items'] = [{"order_id": 3, "product_id": 3, "name": "Rice", "quantity": 1, "price": "4.50"}]
        data = json.dumps(new_order)
        resp =self.app.post('/orders', data=data, content_type="text/plain")
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_item_with_no_name(self):
        """ Create item with no name """        
        order_count = self.get_order_count()
        item_count = self.get_item_count()
        new_order = {'customer_id': 1, 'date': "2018-03-01 18:55:36.985524", 'status': 'processing'}
        new_order['items'] = [{"order_id": 3, "product_id": 3, "quantity": 1, "price": "4.50"}]
        data = json.dumps(new_order)
        resp =self.app.post('/orders', data=data, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order(self):
        """ Update an existing Order """
        order = Order.find_by_customer_id(1)[0]
        new_order = {'customer_id': 1, 'date': "2018-03-01 18:55:36.985524", 'status': 'shipped'}
        new_order['items'] = [{"order_id": 3, "product_id": 3, "name": "Rice", "quantity": 1, "price": "4.50"}]
        data = json.dumps(new_order)
        resp = self.app.put('/orders/{}'.format(order.id), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['status'], 'shipped')

    def test_delete_order(self):
        """ Deleting an Order """
        order = Order.find_by_customer_id(1)[0]
        # Save the current number of orders for assertion
        order_count = self.get_order_count()
        resp = self.app.delete('/orders/{}'.format(order.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_order_count()
        self.assertEqual(new_count, order_count - 1)

    def test_update_item(self):
        """ Update an existing Item """
        item = Item.find_by_name('toilet paper')[0]
        new_item = {'order_id': 1, 'product_id': 2, 'name': "wrench", 'quantity': 1, 'price': 11.50}
        data = json.dumps(new_item)
        resp = self.app.put('/orders/{}/items/{}'.format(new_item['order_id'], item.id), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['name'], 'wrench')

    def test_delete_item(self):
        """ Deleting an Item """
        item = Item.find_by_name('toilet paper')[0]
        
        # Save the current number of items for assertion
        item_count = self.get_item_count()
        resp = self.app.delete('/orders/{}/items/{}'.format(item.order_id, item.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_item_count()
        self.assertEqual(new_count, item_count - 1)

    def test_cancel_order(self):
        """ Cancel an existing Order """
        resp = self.app.put('/orders/1/cancel', content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['status'], 'cancelled')
    
    def test_method_not_allowed(self):
        """ Call a Method thats not Allowed """
        resp = self.app.post('/orders/0')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


######################################################################
# UTILITY FUNCTIONS
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
# MAIN
######################################################################
if __name__ == '__main__':
    unittest.main()
