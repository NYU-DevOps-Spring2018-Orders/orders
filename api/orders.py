import logging

from flask import Blueprint, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes

orders = Blueprint('orders', __name__)

from models import Order
from app import app
# from app import db

def check_content_type(content_type):
    """ Checks that the media type is correct """
    print request.headers['Content-Type']
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(415, 'Content-Type must be {}'.format(content_type))


@orders.route('/orders', methods=['GET'])
def index():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

######################################################################
# RETRIEVE A order
######################################################################
@orders.route('/orders/<int:order_id>', methods=['GET'])
def get_orders(order_id):
    """
    Retrieve a single order

    This endpoint will return a order based on it's id
    """
    order = Order.get(order_id)

    if not order:
        raise NotFound("order with id '{}' was not found.".format(order_id))
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW order
######################################################################
@orders.route('/orders', methods=['POST'])
def create_orders():
    """
    Creates a order
    This endpoint will create a order based the data in the body that is posted
    """
    check_content_type('application/json')
    order = Order()

    """
    test = request.get_json()
    a = test["test"]
    for i in a:
        print i
    """

    order.deserialize(request.get_json())
    order.save()
    message = order.serialize()
    location_url = url_for('get_orders', order_id=order.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
                         })
