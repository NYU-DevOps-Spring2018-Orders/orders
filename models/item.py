import logging

from app import db

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    def __init__(self, statement):
        print statement

class Item(db.Model):
    """ Model for an Item """
    logger = logging.getLogger(__name__)

    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
                "product_id": self.product_id,
                "name": self.name,
                "quantity": self.quantity,
                "price": self.price
                }

    def deserialize(self, data):
        """
        Deserializes an Item from a dictionary

        Args:
            data (dict): A dictionary containing the Item data

        Returns:
            self: instance of Item

        Raises:
            DataValidationError: when bad or missing data
        """
        if not isinstance(data, dict):
            raise DataValidationError('Invalid item: body of request contained bad or no data')
        try:
            self.product_id = data['product_id']
            self.name = data['name']
            self.quantity = data['quantity']
            self.price = data['price']
        except KeyError as error:
            raise DataValidationError('Invalid item: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid item: body of request contained' \
                                      'bad or no data')
        return self

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
