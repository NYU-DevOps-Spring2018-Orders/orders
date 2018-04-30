import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    def __init__(self, statement):
        print statement

class Item(db.Model):
    """ Model for an Item """
    logger = logging.getLogger(__name__)
    app = None

    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Item %r>' % (self.name)

    def save(self):
        """ Saves an Item to the database """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Deletes an Item from the database """
        if self.id:
            db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """
        Serializes an Item into a dictionary

        Returns:
            dict
        """
        return {
                "id": self.id,
                "order_id": self.order_id,
                "product_id": self.product_id,
                "name": self.name,
                "quantity": self.quantity,
                "price": self.price,
                }

    def deserialize(self, data, order_id):
        """
        Deserializes an Item from a dictionary

        Args:
            data (dict): A dictionary containing the Item data

        Returns:
            self: instance of Item

        Raises:
            DataValidationError: when bad or missing data
        """
        try:
            self.order_id = order_id
            self.product_id = data['product_id']
            self.name = data['name']
            self.quantity = data['quantity']
            self.price = data['price']

        except KeyError as error:
            raise DataValidationError('Invalid item: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid item: body of request contained ' \
                                      'bad or no data')
        return self

    @staticmethod
    def init_db(app):
        """ Initializes the database session """
        Item.logger.info('Initializing database')
        Item.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @staticmethod
    def all():
        """
        Fetch all of the Items in the database

        Returns:
            List: list of Items
        """
        Item.logger.info('Processing all Items')
        return Item.query.all()

    @staticmethod
    def get(item_id):
        """
        Get an Item by id

        Args:
            item_id: primary key of items

        Returns:
            Item: item with associated id
        """
        Item.logger.info('Processing lookup for id %s ...', item_id)
        return Item.query.get(item_id)

    @staticmethod
    def get_or_404(item_id):
        """ Finds a Item by it's id """
        Item.logger.info('Processing lookup or 404 for id %s ...', item_id)
        return Item.query.get_or_404(item_id)

    @staticmethod
    def find_by_product_id(product_id):
        """ Returns all Items with the given product_id

        Args:
            product_id (integer): the product_id of the Items you want to match
        """
        Item.logger.info('Processing product_id query for %s ...', product_id)
        return Item.query.filter(Item.product_id == product_id)

    @staticmethod
    def find_by_order_id(order_id):
        """ Returns all Items with the given order_id

        Args:
            order_id (integer): the order_id associated with a list of items
        """
        Item.logger.info('Processing order_id query for %s ...', order_id)
        return Item.query.filter(Item.order_id == order_id)

    @staticmethod
    def find_by_name(name):
        """ Return all Items with the given name

        Args:
            name (string): the name of the Items you want to match
        """
        Item.logger.info('Processing name query for %s ...', name)
        return Item.query.filter(Item.name == name)

    @staticmethod
    def find_by_quantity(quantity):
        """ Return all Items with the given quantity

        Args:
            quantity (integer): the quantity of the Items you want to match
        """
        Item.logger.info('Processing quantity query for %s ...', quantity)
        return Item.query.filter(Item.quantity == quantity)

    @staticmethod
    def find_by_price(price):
        """ Return all Items with the given price

        Args:
            price (float): the price of the Items you want to match
        """
        Item.logger.info('Processing price query for %s ...', price)
        return Item.query.filter(Item.price == price)


class Order(db.Model):
    """ Model for an Item """
    logger = logging.getLogger(__name__)
    app = None

    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Order>'

    def save(self):
        """ Saves an Order to the database """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Deletes an Order and its items from the Database """

        if self.id:
            items = Item.find_by_order_id(self.id)
            for item in items:
                item.delete()
            db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """
        Serializes an Order into a dictionary

        Returns:
            dict
        """
        return {
                "id": self.id,
                "customer_id": self.customer_id,
                "date": self.date,
                "status":self.status
                }

    def deserialize(self, data):
        """
        Deserializes an Order from a dictionary

        Args:
            data (dict): A dictionary containing the Order data

        Returns:
            self: instance of Order

        Raises:
            DataValidationError: when bad or missing data
        """
        try:
            self.customer_id = int(data['customer_id'])
            self.date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M")
            self.status = data['status']

        except KeyError as error:
            raise DataValidationError('Invalid order: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid order: body of request contained ' \
                                      'bad or no data')
        return self

    @staticmethod
    def init_db(app):
        """ Initializes the database session """
        Order.logger.info('Initializing database')
        url = 'With URL {}'.format(app.config['SQLALCHEMY_DATABASE_URI'])
        Order.logger.info(url)
        Order.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @staticmethod
    def remove_all():
        """ Removes all Orders from the database """
        Item.query.delete()
        db.session.commit()
        Order.query.delete()
        db.session.commit()

        db.drop_all()
        db.create_all()

    @staticmethod
    def all():
        """
        Fetch all of the Orders in the database

        Returns:
            List: list of Orders
        """
        Order.logger.info('Processing all Orders')
        return Order.query.all()

    @staticmethod
    def get(order_id):
        """
        Get an Order by id

        Args:
            order_id: primary key of orders

        Returns:
            Order: order with associated id
        """
        Order.logger.info('Processing lookup for id %s ...', order_id)
        return Order.query.get(order_id)

    @staticmethod
    def get_or_404(order_id):
        """ Finds a Order by it's id """
        Order.logger.info('Processing lookup or 404 for id %s ...', order_id)
        return Order.query.get_or_404(order_id)

    @staticmethod
    def find_by_customer_id(customer_id):
        """ Returns all Orders placed by the given customer

        Args:
            customer_id (integer): the customer's id
        """
        Order.logger.info('Processing customer_id query for %s ...', customer_id)
        return Order.query.filter(Order.customer_id == customer_id)

    @staticmethod
    def find_by_date(date):
        """ Returns all Orders with the given date

        Args:
            date (DateTime): the date of the Orders you want to match
        """
        date_converted = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        Order.logger.info('Processing date query for %s ...', date_converted)
        return Order.query.filter(Order.date == date_converted)

    @staticmethod
    def find_by_status(order_status):
        """ Query that finds Orders by their shipping status """
        """ Returns all Orders by their shipping status

        Args:
            status (string): 'processing', 'cancelled', 'shipped'
        """
        Order.logger.info('Processing available query for %s ...', order_status)
        return Order.query.filter(Order.status == order_status)
