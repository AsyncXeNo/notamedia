import config as _

import json
from functools import wraps
from bson import ObjectId

import jwt
from flask import Flask, request
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from loguru import logger

from models import collections
from models.user import User, UserType
from utils.users import require_user_type, user_login, user_registration, create_new_client_user, user_deletion, user_updation
from mongo import setup


HOST = 'localhost'
PORT = 12345

client, database = setup()
client: MongoClient
database: Database

app = Flask(__name__)


"""
ROUTES
"""

@app.route('/users/login', methods=['POST'])
def login():
    payload = json.loads(request.data)
    return user_login(database, payload)


@app.route('/users/new', methods=['POST'])
@require_user_type(database, UserType.SUPER_ADMIN)
def register_user(current_user):
    payload = json.loads(request.data)
    return user_registration(current_user, database, payload)


@app.route('/users/delete', methods=['DELETE'])
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_user(current_user):
    payload = json.loads(request.data)
    return user_deletion(current_user, database, payload)


@app.route('/users/update', methods=['PUT'])
@require_user_type(database, UserType.SUPER_ADMIN)
def update_user(current_user):
    payload = json.loads(request.data)
    return user_updation(current_user, database, payload)


if __name__ == '__main__':
    
    import logging
    # logging.basicConfig(filename='logs/flask.log', level=logging.DEBUG)   

    logger.info(f'starting server: {HOST}:{PORT}')
    
    app.run(
        host=HOST,
        port=PORT,
        debug=False
    )