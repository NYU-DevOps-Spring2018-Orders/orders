import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from flasgger import Swagger
from app.models import Order, Item, DataValidationError
from app import app
from werkzeug.exceptions import NotFound


"""
Order API Controller
This modules provides a REST API for the Order Model
"""

######################################################################
# Swagger Config
######################################################################
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "specs": [
        {
            "version": "1.0.0",
            "title": "Orders Microservice Swagger App",
            "description": "This is a microservice for orders.",
            "endpoint": 'v1_spec',
            "route": '/v1/spec'
        }
    ]
}

# Initialize Swagger after configuring it
Swagger(app)


######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)

@app.errorhandler(400)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=400, error='Bad Request', message=message), 400

@app.errorhandler(404)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=404, error='Not Found', message=message), 404

@app.errorhandler(405)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=405, error='Method not Allowed', message=message), 405

@app.errorhandler(415)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=415, error='Unsupported media type', message=message), 415

@app.errorhandler(500)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=500, error='Internal Server Error', message=message), 500


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Root URL response """
    return app.send_static_file('index.html')


######################################################################
# CREATE A NEW ORDER
######################################################################
@app.route('/orders', methods=['POST'])
def create_order():
    """
    Creates an Order object based on the JSON posted
    This endpoint will create an Order based the data in the body that is posted
    ---
    tags:
      - Orders
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: data
          required:
            - customer_id
            - status
            - date
          properties:
            customer_id:
              type: integer
              description: the customer id for the order
            status:
              type: string
              description: the order status
            date:
              type: string
              description: the date of the order
            items:
              type: array
              items:
                properties:
                    name:
                        type: string
                        description: the item name
                    product_id:
                        type: integer
                        description: the product_id of the item
                    quantity:
                        type: integer
                        description: the quantity of the item
                    price:
                        type: number
                        description: the price of the item
    responses:
      201:
        description: Order created
        schema:
          $ref: '#/definitions/Order'
      400:
        description: Bad Request (the posted data was not valid)
    """

    check_content_type('application/json')
    order = Order()
    json_post = request.get_json()

    order.deserialize(json_post)
    order.save()
    message = order.serialize()

    """
    Want to get the items from POST and create items associated
    with order
    """
    current_order_id = message['id']
    items = json_post['items']
    items_response = []
    for item_dict in items:
        item = Item()
        item.deserialize(item_dict, current_order_id)
        item.save()
        items_response.append(item.serialize())
    """
    The individual responses during the loop were added to a list
    so that the responses can be added to the POST response
    """
    message['items'] = items_response

    location_url = url_for('get_orders', order_id=order.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                            'Location': location_url
                         })


######################################################################
# RETRIEVE A ORDER
######################################################################
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_orders(order_id):
    """
    Retrieve a single Order
    This endpoint will return an Order based on it's id
    ---
    tags:
      - Orders
    produces:
      - application/json
    parameters:
      - name: order_id
        in: path
        description: ID of order to retrieve
        type: integer
        required: true
    responses:
      200:
        description: Order details returned
        schema:
          $ref: '#/definitions/Order'
      404:
        description: Order not found
    """
    order = Order.get(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


######################################################################
# RETRIEVE AN ITEM
######################################################################
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """
    Retrieve a single Item

    This endpoint will return a Item based on it's id
    ---
    tags:
      - Items
    produces:
      - application/json
    parameters:
      - name: item_id
        in: path
        description: ID of item to retrieve
        type: integer
        required: true
    responses:
      200:
        description: Item details returned
        schema:
          $ref: '#/definitions/Item'
      404:
        description: Item not found
    """
    item = Item.get(item_id)
    if not item:
        raise NotFound("Item with id '{}' was not found.".format(item_id))
    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)


######################################################################
# LIST ALL ITEMS
######################################################################
@app.route('/items', methods=['GET'])
def list_items():
    """ Returns all of the Items
    ---
    tags:
      - Items
    description: The Items endpoint allows you to query Items
    parameters:
      - name: order_id
        in: query
        description: the order_id of the Item you are looking for
        required: false
        type: integer
      - name: product_id
        in: query
        description: the product_id of the Item you are looking for
        required: false
        type: integer
      - name: quantity
        in: query
        description: the quantity of the Item you are looking for
        required: false
        type: integer
      - name: price
        in: query
        description: the price of the Item you are looking for
        required: false
        type: number
      - name: name
        in: query
        description: the name of the Item you are looking for
        required: false
        type: string
    definitions:
      Item:
        type: object
        properties:
          id:
            type: integer
            description: unique id assigned internally by service
          name:
            type: string
            description: the item name
          order_id:
            type: integer
            description: the order_id of the item
          product_id:
            type: integer
            description: the product_id of the item
          quantity:
            type: integer
            description: the quantity of the item
          price:
            type: number
            description: the price of the item
    responses:
      200:
        description: An array of Items
        schema:
          type: array
          items:
            schema:
              $ref: '#/definitions/Item'
    """
    items = []

    order_id = request.args.get('order_id')
    product_id = request.args.get('product_id')
    quantity = request.args.get('quantity')
    price = request.args.get('price')
    name = request.args.get('name')

    if order_id:
        items = Item.find_by_order_id(order_id)
    elif product_id:
        items = Item.find_by_product_id(product_id)
    elif quantity:
        items = Item.find_by_quantity(quantity)
    elif price:
        items = Item.find_by_price(price)
    elif name:
        items = Item.find_by_name(name)
    else:
        items = Item.all()

    results = [item.serialize() for item in items]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# LIST ALL ORDERS
######################################################################
@app.route('/orders', methods=['GET'])
def list_orders():
    """ Returns all of the Orders
    ---
    tags:
      - Orders
    description: The Orders endpoint allows you to query Orders
    parameters:
      - name: customer_id
        in: query
        description: the customer_id of the Order you are looking for
        required: false
        type: integer
      - name: status
        in: query
        description: the status of the Order
        required: false
        type: string
      - name: date
        in: query
        description: the Order date
        required: false
        type: string
    definitions:
      Order:
        type: object
        properties:
          id:
            type: integer
            description: unique id assigned internally by service
          customer_id:
            type: integer
            description: the customer id for the order
          status:
            type: string
            description: the order status
          date:
            type: string
            description: the date of the order
    responses:
      200:
        description: An array of Orders
        schema:
          type: array
          items:
            schema:
              $ref: '#/definitions/Order'
    """
    orders = []
    customer_id = request.args.get('customer_id')
    order_status = request.args.get('status')
    date = request.args.get('date')

    if customer_id:
        orders = Order.find_by_customer_id(customer_id)
    elif order_status:
        orders = Order.find_by_status(order_status)
    elif date:
        orders = Order.find_by_date(date)
    else:
        orders = Order.all()

    results = [order.serialize() for order in orders]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# LIST ALL ITEMS FROM AN ORDER
######################################################################
@app.route('/orders/<int:order_id>/items', methods=['GET'])
def list_items_from_an_order(order_id):
    """ Returns all items from an Order
    ---
    tags:
      - Orders
    produces:
      - application/json
    description: The Orders endpoint allows you to query Orders to get all items in that order
    parameters:
      - name: order_id
        in: path
        description: ID of Order to retrieve
        type: integer
        required: true
    responses:
      200:
        description: An array of Items in an order
        schema:
          type: array
          items:
            schema:
              $ref: '#/definitions/Items'
    """
    items = Item.find_by_order_id(order_id)

    results = [item.serialize() for item in items]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# DELETE AN ORDER
######################################################################
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """
    Delete an Order

    This endpoint will delete an Order based on the id specified in
    the path.  It will also delete the items associated with the order
    ---
    tags:
      - Orders
    description: Deletes an Order from the database
    parameters:
      - name: order_id
        in: path
        description: ID of the order to delete
        type: integer
        required: true
    responses:
      204:
        description: Order deleted
    """
    order = Order.get(order_id)
    if order:
        order.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)


######################################################################
# DELETE AN ITEM FROM AN ORDER
######################################################################
@app.route('/orders/<int:order_id>/items/<int:item_id>', methods=['DELETE'])
def delete_item(order_id, item_id):
    """
    Delete an Item
    This endpoint will delete an Item based on the id specified in
    the path
    ---
    tags:
      - Items
    description: Deletes an Item from an order from the database
    parameters:
      - name: order_id
        in: path
        description: ID of the order with an item to delete
        type: integer
        required: true
      - name: item_id
        in: path
        description: ID of the item from the order that needs deleting
        type: integer
        required: true
    responses:
      204:
        description: Item deleted from order
    """
    item = Item.get(item_id)

    if item is None:
        raise NotFound("Order id '{}' has no item with id '{}'.".format(order_id, item_id))

    check_order_id = item.order_id

    if order_id != check_order_id:
        raise NotFound("Order id '{}' does not have item with id '{}'.".format(order_id, item_id))

    if item:
        item.delete()

    return make_response('', status.HTTP_204_NO_CONTENT)


######################################################################
# UPDATE AN ORDER
######################################################################
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_orders(order_id):
    """
    Update an Order

    This endpoint will update an Order based on the body that is posted
    ---
    tags:
      - Orders
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - name: order_id
        in: path
        description: ID of the order that needs updating
        type: integer
        required: true
      - in: body
        name: body
        schema:
          id: data
          required:
            - customer_id
            - status
            - date
          properties:
            customer_id:
                type: integer
                description: the customer id for the order
            status:
                type: string
                description: the order status
            date:
                type: string
                description: the date of the order
    responses:
      200:
        description: Order updated
        schema:
          $ref: '#/definitions/Order'
      400:
        description: Bad Request (the posted data was not valid)
    """
    check_content_type('application/json')
    order = Order.get(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    order.deserialize(request.get_json())
    order.id = order_id
    order.save()
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


######################################################################
# UPDATE AN ITEM
######################################################################
@app.route('/orders/<int:order_id>/items/<int:item_id>', methods=['PUT'])
def update_items(order_id, item_id):
    """
    Update an Item

    This endpoint will update an Item for an order based on the body that is posted
    ---
    tags:
      - Items
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - name: order_id
        in: path
        description: ID of the order that has item to be updated
        type: integer
        required: true
      - name: item_id
        in: path
        description: ID of the item that needs updating of a specified order
        type: integer
        required: true
      - in: body
        name: body
        schema:
          id: data
          required:
            - name
            - product_id
            - quantity
            - price
          name:
            type: string
            description: the item name
          product_id:
            type: integer
            description: the product_id of the item
          quantity:
            type: integer
            description: the quantity of the item
          price:
            type: number
            description: the price of the item
    responses:
      200:
        description: Item updated
        schema:
          $ref: '#/definitions/Item'
      400:
        description: Bad Request (the posted data was not valid)
    """
    check_content_type('application/json')
    item = Item.get(item_id)
    if not item:
        raise NotFound("Item with id '{}' was not found.".format(item_id))
    item.deserialize(request.get_json(), order_id)
    item.id = item_id
    item.save()
    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)


######################################################################
# CANCEL AN ORDER
######################################################################
@app.route('/orders/<int:order_id>/cancel', methods=['PUT'])
def cancel_orders(order_id):
    """
    Cancel an Order

    This endpoint will update an Order based the body that is posted
    ---
    tags:
      - Orders
    description: Changes the status of an order to cancelled
    parameters:
      - name: order_id
        in: path
        description: ID of the order that should be canceled
        type: integer
        required: true
    responses:
      204:
        description: Order cancelled
    """
    order = Order.get(order_id)
    if not order:
        abort(HTTP_404_NOT_FOUND, "Order with id '{}' was not found.".format(order_id))
    order.status = 'cancelled'
    order.save()
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE ALL ORDER DATA (for testing only)
######################################################################
@app.route('/orders/reset', methods=['DELETE'])
def orders_reset():
    """ Removes all orders from the database """
    Order.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
# UTILITY FUNCTIONS
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Order.init_db()

# # load sample data
def data_load(data):
    order = Order()
    order.deserialize(data)
    order.save()

# load sample data
# def data_load(payload):
#     """ Loads a Order into the database """
#     order = Order(0, payload['customer_id'], payload['date'], payload['status'])
#     order.save()

def data_reset():
    """ Removes all Orders from the database """
    Order.remove_all()

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(415, 'Content-Type must be {}'.format(content_type))

def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print 'Setting up logging...'
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info('Logging handler established')
