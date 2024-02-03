from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from bson import ObjectId

import jwt
from flask import request, Request
from pymongo.database import Database

from env import get_var
from models.user import User, UserType
from models import collections


def generate_hash(password: str) -> str:
    return generate_password_hash(password)


def check_hash(password: str, hash: str) -> bool:
    return check_password_hash(hash, password)


def generate_jwt_token(user_id: ObjectId | str, user_name: str, user_type: int, expiration_minutes: int = 60) -> str:
    payload = {
        "user_id": str(user_id),
        "user_name": user_name,
        "user_type": user_type,
        "exp": datetime.utcnow() + timedelta(minutes=expiration_minutes)
    }
    token = jwt.encode(payload, get_var('SECRET_KEY'), algorithm='HS256')
    return token


def verify_jwt_token(token: str) -> (bool, dict):
    try:
        payload = jwt.decode(token, get_var('SECRET_KEY'), algorithms=['HS256'])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, {
            "payload": None,
            "status": "error",
            "message": 'Token has expired'
        }
    except jwt.InvalidTokenError:
        return False, {
            "payload": None,
            "status": "error",
            "message": 'Invalid token'
        }
    

def require_user_type(database: Database, *types):

    def decorator(func):

        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')

            if not token:
                return {
                    "payload": None,
                    "status": "error",
                    "message": "Unauthorized"
                }, 401
            
            token = token.split(' ')[-1]
            
            valid, payload = verify_jwt_token(token)
            if not valid:
                return payload, 401

            user_id = payload["user_id"]
            user_type = payload["user_type"]

            if user_type not in (type.value for type in types):
                return {
                    "payload": None,
                    "status": "error",
                    "message": "Insufficient priviledges"
                }, 403
            
            user = database.get_collection(collections[User]).find_one({ '_id': ObjectId(user_id) })
            
            if not user["active"]:
                return {
                    "payload": None,
                    "status": "error",
                    "message": "User has been disabled"
                }, 403
            
            return func(user, *args, **kwargs)

        return wrapper
    
    return decorator


def user_login(database: Database, payload: dict) -> (dict, int):

    if not payload.get('username') or not payload.get('password'):
        return {
            "payload": None,
            "status": "error",
            "message": "Incomplete credentials"
        }, 400

    users_collection = database.get_collection(collections[User])
    user = users_collection.find_one({ 'name': payload['username'] })

    if not user:
        return {
            "payload": None,
            "status": "error",
            "message": "User does not exist"
        }, 401

    password = payload['password']
    if not check_hash(password, user['hashed_password']):
        return {
            "payload": None,
            "status": "error",
            "message": "Incorrect password"
        }, 401
    
    if not user['active']:
        return {
            "payload": None,
            "status": "error",
            "message": "User has been disabled"
        }, 401
    
    return {
        "payload": {
            "name": user['name'],
            "type": UserType.get_str(user['user_type']),
            "token": generate_jwt_token(user['_id'], user['name'], user['user_type'])
        },
        "status": "success",
        "message": "Successfully logged in"
    }, 200


def user_registration(database: Database, payload: dict) -> (dict, int):

    if not payload.get('username') or not payload.get('password') or not payload.get('user_type') or not payload.get('is_active'):
        return {
            "payload": None,
            "status": "error",
            "message": "Incomplete information"
        }, 400
    
    username = payload['username']
    password = payload['password']
    user_type = payload['user_type']    
    is_active = payload['is_active']
    hashed_password = generate_hash(password)

    users_collection = database.get_collection(collections[User])

    existing_user = users_collection.find_one({ "name": username })
    if existing_user:
        return {
            "payload": None,
            "status": "error",
            "message": "Username already exists"
        }, 409

    if user_type not in (type.value for type in [UserType.SUPER_ADMIN, UserType.WORKER]):
        return {
            "payload": None,
            "status": "error",
            "message": "Invalid user type"
        }, 400

    user = User(
        username,
        hashed_password,
        user_type,
        is_active
    )

    user = users_collection.insert_one(user.to_dict())

    if user.acknowledged:
        return {
            "payload": {
                "user_id": str(user['_id']),
                "username": user['name'],
                "is_active": user['active']
            },
            "status": "success",
            "message": "User registered successfully"
        }, 201
    
    return {
        "payload": None,
        "status": "error",
        "message": "User registration failed"
    }, 500
    