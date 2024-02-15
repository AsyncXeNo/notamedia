from bson import ObjectId
from typing import Tuple

from loguru import logger
from pymongo.database import Database

from views.response import Response
from models import collections
from models.product import ProductType, Product
from models.price import Price


"""
PRODUCT TYPES
"""


def product_type_creation(current_user: dict, database: Database, payload: dict) -> Tuple[dict, int]:

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


def product_type_deletion(current_user: dict, database: Database, payload: dict) -> Tuple[dict, int]:
    
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


def all_product_types(database: Database) -> Tuple[dict, int]:
    
    product_types_collection = database.get_collection(collections[ProductType])

    product_types = list(product_types_collection.find())
    for product_type in product_types:
        product_type['_id'] = str(product_type['_id'])

    return {
        "payload": product_types,
        "status": "success",
        "message": ""
    }, 200


"""
PRODUCTS
"""


def product_creation(current_user: dict, database: Database, payload: dict) -> Response:
    
    try:
        unique_name = payload['unique_name']
        product_type_id = payload['product_type_id']
        item_description = payload['item_description']
        particulars = payload['particulars']
        default_quantity = payload['default_quantity']
        fixed_quantity = payload['fixed_quantity']
        unit = payload['unit']
        base_price = payload['base_price']
        implementation_fee = payload['implementation_fee']
        default_vendor_discount = payload['default_vender_discount']
        description_left = payload['description_left']
        description_right = payload['description_right']
    except KeyError:
        return Response(400, 'error', message='Incomplete information')
    
    try:
        base_price = Price(base_price['inr'], base_price['usd'], base_price['aed'], base_price['eur'], base_price['gbp'])
    except KeyError:
        return Response(400, 'error', message='Invalid base price')
    
    try:
        implementation_fee = Price(implementation_fee['inr'], implementation_fee['usd'], implementation_fee['aed'], implementation_fee['eur'], implementation_fee['gbp'])
    except KeyError:
        return Response(400, 'error', message='Invalid implementation fee')
    
    products_collection = database.get_collection(collections.get(Product))

    existing_product = products_collection.find_one({ 'unique_name': unique_name })
    if existing_product:
        return Response(409, 'error', message='Product already exists')
    
    product_types_collection = database.get_collection(collections.get(ProductType))
    product_type = product_types_collection.find_one({ '_id': ObjectId(product_type_id) })
    if not product_type:
        return Response(404, 'error', message='Product type not found')

    del(product_type['_id'])
    
    product = Product(
        unique_name,
        product_type,
        item_description,
        particulars,
        default_quantity,
        fixed_quantity,
        unit,
        base_price,
        implementation_fee,
        default_vendor_discount,
        description_left,
        description_right
    )

    inserted = products_collection.insert_one(product.to_dict())

    if inserted.acknowledged:
        logger.debug(f'new product created ("{unique_name}") by user named "{current_user["name"]}"')
        return Response(201, 'success', payload={
                            'unique_name': unique_name
                        })
    
    return Response(500, 'error', message='Product creation failed')


def product_updation(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('unique_name') or not payload.get('new'):
        return Response(400, 'error', message='Incomplete information')
    
    unique_name = payload['unique_name']
    new = payload['new']

    products_collection = database.get_collection(collections.get(Product))

    existing_product = products_collection.find_one({ 'unique_name': unique_name })
    if not existing_product:
        return Response(404, 'error', message='Product not found')
    
    for key in new.keys():
        if key not in existing_product.keys():
            return Response(400, "error", message=f"Invalid attribute to update: {key}")

    if new.get('_id'):
        return Response(400, "error", message=f"Invalid attribute to update: _id")
    
    if new.get('unique_name'):
        return Response(400, "error", message=f"Invalid attribute to update: unique_name")
    
    if new.get('product_type_id'):
        product_type_id = new['product_type_id']
        product_types_collection = database.get_collection(collections.get(ProductType))
        product_type = product_types_collection.find_one({ '_id': ObjectId(product_type_id) })
        if not product_type:
            return Response(404, 'error', 'Product type not found')
        del(product_type['_id'])
        new['product_type'] = product_type
        del(new['product_type_id'])

    updated = products_collection.update_one({ 'unique_name': unique_name }, { '$set': new })

    if updated.acknowledged:
        logger.info(f'product named "{unique_name}" has been updated by user named "{current_user["name"]}"')

        return Response(200, 'success', message='Product updated successfully')
    
    return Response(500, 'error', 'Product updation failed')


def product_deletion(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('unique_name'):
        return Response(400, 'error', message='Incomplete information')
    
    unique_name = payload['unique_name']

    products_collection = database.get_collection(collections.get(Product))

    existing_product = products_collection.find_one({ 'unique_name': unique_name })
    if not existing_product:
        return Response(404, 'error', message='Product not found')

    products_collection.delete_one({ 'unique_name': unique_name }) 
    logger.warning(f'product named "{unique_name}" deleted by user named "{current_user["name"]}"')

    return Response(204, 'success', message='Product deleted successfully')


def product_existing(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('unique_name'):
        return Response(400, 'error', message='Incomplete information')
    
    unique_name = payload['unique_name']

    products_collection = database.get_collection(collections.get(Product))

    existing_product = products_collection.find_one({ 'unique_name': unique_name })
    if not existing_product:
        return Response(404, 'error', message='Product not found')
    
    del(existing_product['_id'])

    return Response(200, 'success', payload=existing_product)


def all_products(database: Database) -> Response:
    
    products_collection = database.get_collection(collections.get(Product))
    products = list(products_collection.find())

    for product in products:
        product['_id'] = str(product['_id'])

    return Response(200, 'success', payload=products)
    