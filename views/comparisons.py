from loguru import logger
from pymongo.database import Database

from models import collections
from models.comparison import Comparison
from views.response import Response


def comparison_creation(current_user: dict, database: Database, payload: dict) -> Response:
    
    try:
        title = payload['title']
        table_data = payload['table_data']
        summary = payload['summary']
    except KeyError:
        return Response(400, 'error', message='Incomplete information')

    if not title or not table_data or not summary:
        return Response(400, "error", message="Incomplete information")
    
    comparisons_collection = database.get_collection(collections.get(Comparison))

    existing_comparison = comparisons_collection.find_one({ 'title': title })
    if existing_comparison:
        return Response(409, 'error', message='Comparison already exists')
    
    comparison = Comparison(
        title,
        table_data,
        summary
    )

    inserted = comparisons_collection.insert_one(comparison.to_dict())

    if inserted.acknowledged:
        logger.debug(f'new comparison titled "{title}" created by user named "{current_user["name"]}"')
        return Response(201, 'success', payload={
                            'title': title
                        })
    
    return Response(500, 'error', message='Something went wrong')


def comparison_updation(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('title') or not payload.get('new'):
        return Response(400, 'error', message='Incomplete information')

    title = payload['title']
    new = payload['new']

    for key in new.keys():
        if key not in ['table_data', 'summary', "title"]:
            return Response(400, "error", message=f"Invalid attribute to update: {key}")
        
    comparisons_collection = database.get_collection(collections.get(Comparison))

    existing_collection = comparisons_collection.find_one({ 'title': title })
    if not existing_collection:
        return Response(404, 'error', message='Comparison not found')
    
    updated = comparisons_collection.update_one({ 'title': title }, { '$set': new })

    if updated.acknowledged:
        logger.debug(f'comparison titled "{title}" updated by user named "{current_user["name"]}"')
        return Response(200, 'success', message='Comparison updated successfully')

    return Response(500, 'error', message='Something went wrong')
    

def comparison_deletion(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('title'):
        return Response(400, 'error', message='Incomplete information')

    title = payload['title']

    comparisons_collection = database.get_collection(collections.get(Comparison))

    existing_collection = comparisons_collection.find_one({ 'title': title })
    if not existing_collection:
        return Response(404, 'error', message='Comparison not found')
    
    comparisons_collection.delete_one({ 'title': title })

    logger.warning(f'comparison titled {title} deleted by user named "{current_user["name"]}"')

    return Response(200, 'success', message='Comparison successfully deleted')
    

def comparison_existing(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('title'):
        return Response(400, 'error', message='Incomplete information')

    title = payload['title']

    comparisons_collection = database.get_collection(collections.get(Comparison))

    existing_collection = comparisons_collection.find_one({ 'title': title })
    if not existing_collection:
        return Response(404, 'error', message='Comparison not found')
    
    del(existing_collection['_id'])
    
    return Response(200, 'success', payload=existing_collection)
    

def all_comparisons(database: Database) -> Response:
    
    comparisons_collection = database.get_collection(collections.get(Comparison))
    comparisons = list(comparisons_collection.find())

    for comparison in comparisons:
        comparison['_id'] = str(comparison['_id'])

    return Response(200, 'success', payload=comparisons)
