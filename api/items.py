import logging

from flask import Blueprint, jsonify, request, url_for, make_response
from flask_api import status    # HTTP Status Codes

items = Blueprint('items', __name__)

@items.route('/items', methods=['GET'])
def index():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
