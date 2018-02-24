import logging

from flask import Blueprint, jsonify, request, url_for, make_response
from flask_api import status    # HTTP Status Codes

orders = Blueprint('orders', __name__)

@orders.route('/orders', methods=['GET'])
def index():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
