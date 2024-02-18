from bson import ObjectId

from loguru import logger
from pymongo.database import Database

from views.response import Response
from models import collections
from models.commercial import PaymentTerms


def payment_terms_creation(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('name') or not payload.get('terms'):
        return Response(400, 'error', 'Incomplete information')
    
    name = payload['name']
    terms = payload['terms']

    payment_terms_collection = database.get_collection(collections.get(PaymentTerms))
    
    existing_terms = payment_terms_collection.find_one({ 'name': name })
    if existing_terms:
        return Response(400, 'error', 'Payment terms already exist')
    
    payment_terms = PaymentTerms(
        name,
        terms
    )

    inserted = payment_terms_collection.insert_one(payment_terms.to_dict())
    if inserted.acknowledged:
        logger.debug(f'new payment terms ("{name}") created by user named "{current_user["name"]}"')
        return Response(201, 'success', 'Payment terms created successfully')

    return Response(500, 'error', 'Payment terms creation failed')


def payment_terms_updation(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('name') or not payload.get('new'):
        return Response(400, 'error', 'Incomplete information')

    name = payload['name']
    new = payload['new']

    payment_terms_collection = database.get_collection(collections.get(PaymentTerms))
    
    existing_terms = payment_terms_collection.find_one({ 'name': name })
    if not existing_terms:
        return Response(404, 'error', 'Payment terms do not exist')
    
    for key in new.keys():
        if key not in ['name', 'terms']:
            return Response(400, "error", message=f"Invalid attribute to update: {key}")
        
    updated = payment_terms_collection.update_one({ 'name': name }, { '$set': new })
    if updated.acknowledged:
        logger.debug(f'payment terms named "{name}" updated by user named "{current_user["name"]}"')
        return Response(200, 'success', 'Payment terms updated successfully')
    
    return Response(500, 'error', 'Payment terms updation failed')
    

def payment_terms_deletion(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('name'):
        return Response(400, 'error', 'Incomplete information')

    name = payload['name']

    payment_terms_collection = database.get_collection(collections.get(PaymentTerms))
    
    existing_terms = payment_terms_collection.find_one({ 'name': name })
    if not existing_terms:
        return Response(404, 'error', 'Payment terms do not exist')
    
    payment_terms_collection.delete_one({ 'name': name })
    logger.warning(f'payment terms named "{name}" deleted by user named "{current_user["name"]}"')

    return Response(200, 'success', 'Payment terms deleted successfully')


def payment_terms_existing(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('name'):
        return Response(400, 'error', 'Incomplete information')

    name = payload['name']

    payment_terms_collection = database.get_collection(collections.get(PaymentTerms))
    
    existing_terms = payment_terms_collection.find_one({ 'name': name })
    if not existing_terms:
        return Response(404, 'error', 'Payment terms do not exist')
    
    existing_terms['_id'] = str(existing_terms['_id'])

    return Response(200, 'success', payload=existing_terms)


def all_payment_terms(database: Database) -> Response:
    
    payment_terms_collection = database.get_collection(collections.get(PaymentTerms))
    terms = list(payment_terms_collection.find())

    for term in terms:
        term['_id'] = str(term['_id'])

    return Response(200, 'success', payload=terms)
