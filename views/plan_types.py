from bson import ObjectId

from loguru import logger
from pymongo.database import Database

from views.response import Response
from models import collections
from models.company import PlanType


def plan_type_creation(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('name'):
        return Response(400, 'error', 'Incomplete information')
    
    name = payload['name']
    
    plan_types_collection = database.get_collection(collections.get(PlanType))
    
    existing_type = plan_types_collection.find_one({ 'name': name })
    if existing_type:
        return Response(409, 'error', 'Plan type already exists')
    
    plan_type = PlanType(name)

    inserted = plan_types_collection.insert_one(plan_type.to_dict())

    if inserted.acknowledged:
        logger.debug(f'New plan type created by user named "{current_user["name"]}"')
        return Response(201, 'success', 'Plan type created successfully')
    
    return Response(500, 'error', 'Plan type creation failed')


def plan_type_deletion(current_user: dict, database: Database, payload: dict) -> Response:

    if not payload.get('name'):
        return Response(400, 'error', 'Incomplete information')
    
    name = payload['name']
    
    plan_types_collection = database.get_collection(collections.get(PlanType))
    
    existing_type = plan_types_collection.find_one({ 'name': name })
    if not existing_type:
        return Response(404, 'error', 'Plan type does not exist')

    plan_types_collection.delete_one({ 'name': name })
    
    return Response(204, 'success', 'Plan type deleted successfully')


def plan_type_existing(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('name'):
        return Response(400, 'error', 'Incomplete information')
    
    name = payload['name']
    
    plan_types_collection = database.get_collection(collections.get(PlanType))
    
    existing_type = plan_types_collection.find_one({ 'name': name })
    if not existing_type:
        return Response(404, 'error', 'Plan type does not exist')
    
    del(existing_type['_id'])

    return Response(200, 'success', payload = existing_type)


def all_plan_types(database: Database) -> Response:
    
    plan_types_collection = database.get_collection(collections.get(PlanType))
    types = list(plan_types_collection.find())

    for type_ in types:
        del(type_['_id'])

    return Response(200, 'succes', payload=types)
