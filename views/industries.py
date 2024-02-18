from loguru import logger
from pymongo.database import Database

from models import collections
from models.industry import Industry
from views.response import Response
from views.image_utils import get_image_info, save_image, get_image, delete_image


def industry_creation(current_user: dict, database: Database, payload: dict) -> Response:
    
    try:
        name = payload['name']
        images = payload['images']
    except KeyError:
        return Response(400, 'error', 'Incomplete information')
    
    if not name or not images:
        return Response(400, 'error', 'Incomplete information')

    industries_collection = database.get_collection(collections.get(Industry))

    existing_industry = industries_collection.find_one({ 'name': name })
    if existing_industry:
        return Response(409, 'error', 'Industry already exists')
    
    restrictions = Industry.get_image_restrictions()
    images_to_save = []
    for image in images:
        img_info = get_image_info(image)
        
        if img_info.get('error'):
            return Response(400, "error", message="Invalid image")
            
        if img_info['format'] not in restrictions['allowed_formats']:
            return Response(400, "error", message=f"Invalid image format: {img_info['format']}")
            
        if img_info['width'] < restrictions['width'][0] or img_info['width'] > restrictions['width'][1] or img_info['height'] < restrictions['height'][0] or img_info['height'] > restrictions['height'][1]:
            return Response(500, "error", message="Error while saving image")
        
        save_info = save_image(image)
        if save_info.get('error'):
            return Response(500, "error", message="Error while saving image")

        images_to_save.append(save_info['filename'])

    industry = Industry(
        name,
        images_to_save
    )

    inserted = industries_collection.insert_one(industry.to_dict())

    if inserted.acknowledged:
        logger.debug(f'new industry ("{name}") created by user named "{current_user["name"]}"')
        return Response(201, 'success', payload={ 'name': name })


    return Response(500, 'error', message='Industry addition failed')


def industry_updation(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('name') or not payload.get('new'):
        return Response(400, "error", message="Incomplete information")

    name = payload.get('name')
    new = payload.get('new')

    name = new.get('name')
    images = new.get('images')

    industries_collection = database.get_collection(collections.get(Industry))

    existing_industry = industries_collection.find_one({ 'name': name })
    if not existing_industry:
        return Response(404, 'error', 'Industry not found')

    if images:
        restrictions = Industry.get_image_restrictions()
        images_to_save = []
        for image in images:
            img_info = get_image_info(image)
            
            if img_info.get('error'):
                return Response(400, "error", message="Invalid image")
                
            if img_info['format'] not in restrictions['allowed_formats']:
                return Response(400, "error", message=f"Invalid image format: {img_info['format']}")
                
            if img_info['width'] < restrictions['width'][0] or img_info['width'] > restrictions['width'][1] or img_info['height'] < restrictions['height'][0] or img_info['height'] > restrictions['height'][1]:
                return Response(500, "error", message="Error while saving image")
            
            save_info = save_image(image)
            if save_info.get('error'):
                return Response(500, "error", message="Error while saving image")

            images_to_save.append(save_info['filename'])

    new = {}
    
    if name:
        new['name'] = name
    if images:
        new['images'] = images_to_save

    updated = industries_collection.update_one({ 'name': name }, { '$set': new })

    if updated.acknowledged:
        logger.debug(f'industry named "{name}" updated by user named "{current_user["name"]}"')

        if images:
            for image in existing_industry['images']:
                delete_image(image)
        
        return Response(200, 'success', 'Industry successfully updated')
    
    return Response(500, 'error', 'Industry updation failed')
    
    
def industry_deletion(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('name'):
        return Response(400, "error", message="Incomplete information")

    name = payload['name']

    industries_collection = database.get_collection(collections.get(Industry))

    existing_industry = industries_collection.find_one({ 'name': name })
    if not existing_industry:
        return Response(404, 'error', 'Industry not found')
    
    for image in existing_industry['images']:
        delete_image(image)

    industries_collection.delete_one({ 'name': name })
    logger.warning(f'industry named "{name}" deleted by user named "{current_user["name"]}"')

    return Response(200, 'success', 'Industry deleted successfully')


def industry_existing(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('name'):
        return Response(400, "error", message="Incomplete information")

    name = payload['name']

    industries_collection = database.get_collection(collections.get(Industry))

    existing_industry = industries_collection.find_one({ 'name': name })
    if not existing_industry:
        return Response(404, 'error', 'Industry not found')
    
    del(existing_industry['_id'])
    encoded_images = []
    for image in existing_industry['images']:
        image_encoded = get_image(image)
        if image_encoded.get('error'):
            return Response(500, "error", message="Error while reading image for industry")
        encoded_images.append(image_encoded.get('data'))

    existing_industry['images'] = encoded_images

    return Response(200, 'success', payload=existing_industry)
    

def all_industries(database: Database) -> Response:
    
    industries_collection = database.get_collection(collections.get(Industry))
    industries = list(industries_collection.find())
    for industry in industries:
        industry['_id'] = str(industry['_id'])
        del(industry['images'])

    return Response(200, 'success', payload=industries)
