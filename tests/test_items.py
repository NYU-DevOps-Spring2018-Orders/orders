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
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_an_item(self):
        """ Create a item and assert that it exists """
        item = Item(product_id=1, name="wrench", quantity=1, price=10.50)

        self.assertEqual(item.id, None)
        self.assertEqual(item.product_id, 1)
        self.assertEqual(item.name, "wrench")
        self.assertEqual(item.quantity, 1)
        self.assertEqual(item.price, 10.50)

    def test_add_an_item(self):
        """ Create an Item and add it to the database """
        items = Item.all()
        self.assertEqual(items, [])
        item = Item(product_id=1, name="wrench", quantity=1, price=10.50)
        self.assertEqual(item.id, None)
        item.save()

        self.assertEqual(item.id, 1)
        items = Item.all()
        self.assertEqual(len(items), 1)

    def test_update_an_item(self):
        """ Update an Item """
        item = Item(product_id=1, name="wrench", quantity=1, price=10.50)
        item.save()
        self.assertEqual(item.id, 1)

        item.price = 12.0
        item.save()

        items = Item.all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].price, 12.0)

    def test_delete_an_item(self):
        """ Delete an Item """
        item = Item(product_id=1, name="wrench", quantity=1, price=10.50)
        item.save()
        self.assertEqual(len(Item.all()), 1)

        item.delete()
        self.assertEqual(len(Item.all()), 0)

    def test_serialize_an_item(self):
        """ Test serialization of an Item """
        item = Item(product_id=1, name="wrench", quantity=1, price=10.50)
        data = item.serialize()

        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], None)

        self.assertIn('product_id', data)
        self.assertEqual(data['product_id'], 1)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "wrench")
        self.assertIn('quantity', data)
        self.assertEqual(data['quantity'], 1)
        self.assertIn('price', data)
        self.assertEqual(data['price'], 10.50)

    def test_deserialize_an_item(self):
        """ Test deserialization of an Item """
        data = {"id": 1, "product_id": 1, "name": "wrench", "quantity": 1, "price": 10.50}
        item = Item()
        item.deserialize(data)

        self.assertNotEqual(item, None)
        self.assertEqual(item.id, None)
        self.assertEqual(item.product_id, 1)
        self.assertEqual(item.name, "wrench")
        self.assertEqual(item.quantity, 1)
        self.assertEqual(item.price, 10.50)

    def test_fetch_all_items(self):
        """ Test fetching all Items """
        item = Item(product_id=1, name="wrench", quantity=1, price=10.50)
        item.save()
        item2 = Item(product_id=2, name="hammer", quantity=2, price=11)
        item2.save()
        Item.all()

        self.assertEqual(len(Item.all()), 2)

    def test_get_an_item(self):
        """ Get an Item by id """
        hammer = Item(product_id=2, name="hammer", quantity=2, price=11)
        hammer.save()

        item = Item.get(hammer.id)

        self.assertEqual(item.id, hammer.id)
        self.assertEqual(item.name, "hammer")

    def test_non_dict_raises_error(self):
        """ Pass invalid data structure deserialize """
        data = [1,2,3]
        item = Item()

        with self.assertRaises(DataValidationError):
            item.deserialize(data)

    def test_invalid_key_raises_error(self):
        """ Try to pass invalid key """
        data = {"id": 1, "product_id": 1, "quantity": 1, "price": 10.50}

        with self.assertRaises(DataValidationError):
            item = Item()
            item.deserialize(data)

    def test_repr(self):
        """ Test that string representation is correct """
        hammer = Item(product_id=2, name="hammer", quantity=2, price=11)
        hammer.save()

        self.assertEqual(hammer.__repr__(), "<Item u'hammer'>")

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
