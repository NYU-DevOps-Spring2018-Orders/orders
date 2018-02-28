import logging

from app import db

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    def __init__(self, statement):
        print statement

class Order(db.Model):
    """ Model for an Item """
    logger = logging.getLogger(__name__)

    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, nullable=False)
    # date = db.Column(db.DateTime, nullable=False)
    shipped = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Order>'

    def save(self):
        """ Saves an Order to the database """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Deletes an Order from the database """
        if self.id:
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
                # "date": self.date,
                "shipped": self.shipped
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
            self.customer_id = data['customer_id']
            # self.date = data['date']
            self.shipped = data['shipped']
        except KeyError as error:
            raise DataValidationError('Invalid order: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid order: body of request contained' \
                                      'bad or no data')
        return self

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
