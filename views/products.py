from loguru import logger
from pymongo.database import Database

from models import collections
from models.product import ProductType


def product_type_creation(current_user: dict, database: Database, payload: dict) -> (dict, int):

    if (not payload.get('name')):
        return {
            "payload": None,
            "status": "error",
            "message": "Incomplete information"
        }, 400
    
    name = payload['name']
    product_types_collection = database.get_collection(collections[ProductType])

    existing_product_type = product_types_collection.find_one({ 'name': name })

    if existing_product_type:
        return {
            "payload": None,
            "status": "error",
            "message": "Product type already exists"
        }, 409

    product_type = ProductType(name)
    inserted = product_types_collection.insert_one(product_type.to_dict())
    
    if inserted.acknowledged:
        logger.debug(f'new product type created ("{name}") by user named "{current_user["name"]}" (LEVEL {current_user["user_type"]})')

        return {
            "payload": {
                "name": name
            },
            "status": "success",
            "message": "Product type created successfully"
        }, 201

    return {
        "payload": None,
        "status": "error",
        "message": "Product type creation failed"
    }, 500


def product_type_deletion(current_user: dict, database: Database, payload: dict) -> (dict, int):
    
    if (not payload.get('name')):
        return {
            "payload": None,
            "status": "error",
            "message": "Incomplete information"
        }, 400
    
    name = payload['name']
    product_types_collection = database.get_collection(collections[ProductType])

    existing_product_type = product_types_collection.find_one({ 'name': name })
    if not existing_product_type:
        return {
            "payload": None,
            "status": "error",
            "message": "Product type not found"
        }, 404
    
    product_types_collection.delete_one({ 'name': name })

    return {
        "payload": None,
        "status": "success",
        "message": "Product type successfully deleted"
    }, 204

def all_product_types(database: Database) -> (dict, int):
    
    product_types_collection = database.get_collection(collections[ProductType])

    product_types = list(product_types_collection.find())
    for product_type in product_types:
        product_type['_id'] = str(product_type['_id'])

    return {
        "payload": product_types,
        "status": "success",
        "message": ""
    }
    