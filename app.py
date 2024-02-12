import config as _

import json
import logging
from functools import wraps
from bson import ObjectId

import jwt
from flask import Flask, request
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from loguru import logger

from models import collections
from models.user import User, UserType
from views.users import require_user_type, user_login, user_registration, create_new_client_user, user_deletion, user_updation, all_users
from views.products import product_type_creation, product_type_deletion, all_product_types
from views.signatures import signature_creation, signature_deletion, signature_updation, all_signatures
from views.response import Response
from mongo import setup


HOST = 'localhost'
PORT = 12345

client, database = setup()
client: MongoClient
database: Database

app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True


"""
USER ROUTES
"""

@app.route('/users/login', methods=['POST'])
def login():

    if not request.data: return Response(400, "error", message="Incomplete information")

    payload = json.loads(request.data)
    return user_login(database, payload)


@app.route('/users/new', methods=['POST'])
@require_user_type(database, UserType.SUPER_ADMIN)
def register_user(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information")
    
    payload = json.loads(request.data)
    return user_registration(current_user, database, payload)


@app.route('/users/delete', methods=['DELETE'])
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_user(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information")

    payload = json.loads(request.data)
    return user_deletion(current_user, database, payload)


@app.route('/users/update', methods=['PUT'])
@require_user_type(database, UserType.SUPER_ADMIN)
def update_user(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information")
    
    payload = json.loads(request.data)
    return user_updation(current_user, database, payload)

@app.route('/users', methods=['GET'])
@require_user_type(database, UserType.SUPER_ADMIN)
def get_users(current_user):

    return all_users(database)


"""
PRODUCT TYPE ROUTES
"""    

@app.route('/products/types/new', methods=['POST'])
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def new_product_type(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information")

    payload = json.loads(request.data)
    return product_type_creation(current_user, database, payload)


@app.route('/products/types/delete', methods=['DELETE'])
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_product_type(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information")

    payload = json.loads(request.data)
    return product_type_deletion(current_user, database, payload)


@app.route('/products/types', methods=['GET'])
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_product_types(current_user):

    return all_product_types(database)


"""
PRODUCT ROUTES
"""

"""
SIGNATURE ROUTES
"""

@app.route('/signatures/new', methods=['POST'])
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def new_signature(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information")
    
    payload = json.loads(request.data)
    return signature_creation(current_user, database, payload).to_response()


@app.route('/signatures/delete', methods=['DELETE'])
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_signature(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information")

    payload = json.loads(request.data)
    return signature_deletion(current_user, database, payload).to_response()


@app.route('/signatures/update', methods=['PUT'])
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def update_signature(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information")

    payload = json.loads(request.data)
    return signature_updation(current_user, database, payload).to_response()


@app.route('/signatures', methods=['GET'])
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_signatures(current_user):

    return all_signatures(database).to_response()
    

if __name__ == '__main__':

    logger.info(f'starting server: {HOST}:{PORT}')
    
    app.run(
        host=HOST,
        port=PORT,
        debug=False
    )