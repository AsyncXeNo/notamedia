from bson import ObjectId

from loguru import logger
from pymongo.database import Database

from views.response import Response
from models import collections
from models.commercial import ProposalType


def proposal_type_creation(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('name'):
        return Response(400, 'error', 'Incomplete information')

    name = payload['name']

    proposal_types_collection = database.get_collection(collections.get(ProposalType))
    
    existing_type = proposal_types_collection.find_one({ 'name': name })
    if existing_type:
        return Response(409, 'error', 'Proposal type already exists')
    
    proposal_type = ProposalType(
        name
    )

    inserted = proposal_types_collection.insert_one(proposal_type.to_dict())

    if inserted.acknowledged:
        logger.debug(f'new proposal type ("{name}") created by user named "{current_user["name"]}"')
        return Response(201, 'success', 'Proposal type created')

    return Response(500, 'error', 'Proposal type creation failed')


def proposal_type_deletion(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('name'):
        return Response(400, 'error', 'Incomplete information')

    name = payload['name']

    proposal_types_collection = database.get_collection(collections.get(ProposalType))
    
    existing_type = proposal_types_collection.find_one({ 'name': name })
    if not existing_type:
        return Response(404, 'error', 'Proposal type does not exists')
    
    proposal_types_collection.delete_one({ 'name': name })
    logger.warning(f'proposal type named "{name}" deleted by user named "{current_user["name"]}"')

    return Response(200, 'success', 'Proposal type deleted successfully')


def all_proposal_types(database: Database) -> Response:
    
    proposal_types_collection = database.get_collection(collections.get(ProposalType))
    types = list(proposal_types_collection.find())

    for type_ in types:
        type_['_id'] = str(type_['_id'])

    return Response(200, 'success', payload=types)