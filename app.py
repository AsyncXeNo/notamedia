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
from utils.users import require_user_type, user_login, user_registration
from mongo import setup


client, database = setup()
client: MongoClient
database: Database

app = Flask(__name__)


"""
ROUTES
"""

@app.route('/users/new', methods=['POST'])
@require_user_type(database, UserType.SUPER_ADMIN)
def register_user(current_user):
    payload = json.loads(request.data)
    return user_registration(payload)
    

@app.route('/users/login', methods=['POST'])
def login():
    payload = json.loads(request.data)
    return user_login(database, payload)


if __name__ == '__main__':
    
    import logging
    logging.basicConfig(filename='logs/flask.log', level=logging.DEBUG)

    logger.info('starting server')
    
    app.run(
        host='localhost',
        port='12345'
    )