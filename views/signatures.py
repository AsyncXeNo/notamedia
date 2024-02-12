from typing import Tuple
from bson import ObjectId

from loguru import logger
from pymongo.database import Database

from models import collections
from models.signature import Signature
from views.image_utils import get_image_info, save_image, delete_image
from views.response import Response


def signature_creation(current_user: dict, database: Database, payload: dict) -> Response:
    
    # Initial validation
    try:
        unique_name = payload['unique_name']
        sender_full_name = payload['sender_full_name']
        sender_short_name = payload['sender_short_name']
        sender_designation = payload['sender_designation']
        sender_phone = payload['sender_phone']
        sender_email = payload['sender_email']
        sender_company_website = payload['sender_company_website']
        sender_picture = payload['sender_picture']
        sender_company_name = payload['sender_company_name']
    except:
        return Response(400, "error", message="Incomplete information")
    
    signatures_collection = database.get_collection(collections[Signature])
    existing_signature = signatures_collection.find_one({ 'unique_name': unique_name })

    if existing_signature:
        return Response(409, "error", message="Signature already exists")
    
    # Process and save picture
    restrictions = Signature.get_image_restrictions()
    img_info = get_image_info(sender_picture)

    if img_info.get('error'):
        return Response(400, "error", message="Invalid image")

    if img_info['format'] not in restrictions['allowed_formats']:
        return Response(400, "error", message=f"Invalid image format: {img_info['format']}")
    
    if img_info['width'] < restrictions['width'][0] or img_info['width'] > restrictions['width'][1] or img_info['height'] < restrictions['height'][0] or img_info['height'] > restrictions['height'][1]:
        return Response(400, "error", message="Invalid image dimensions")
    
    save_info = save_image(sender_picture)
    if save_info.get('error'):
        return Response(500, "error", message="Error while saving image")
    
    sender_picture = save_info['filename']
    
    # Save signature
    signature = Signature(
        unique_name,
        sender_full_name,
        sender_short_name,
        sender_designation,
        sender_phone,
        sender_email,
        sender_company_website,
        sender_picture,
        sender_company_name   
    )

    inserted = signatures_collection.insert_one(signature.to_dict())
    signature = signatures_collection.find_one({ "_id": ObjectId(inserted.inserted_id) })

    if inserted.acknowledged:
        logger.debug(f'new signature added by user named "{current_user["name"]}", signature name: {unique_name}')
        return Response(201, "success",
                        payload={
                            "signature_id": str(signature['_id']),
                            "unique_name": unique_name
                        },
                        message="Signature added successfully")
    
    return Response(500, "error", message="Signature addition failed")


def signature_deletion(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('unique_name'):
        return Response(400, "error", message="Incomplete information")
    
    unique_name = payload.get('unique_name')
    
    signatures_collection = database.get_collection(collections[Signature])
    signature = signatures_collection.find_one({ 'unique_name': unique_name })

    if not signature:
        return Response(404, "error", message="Signature not found")
    
    delete_image(signature['sender_picture'])

    signatures_collection.delete_one({ 'unique_name': unique_name })
    logger.warning(f'signature named "{unique_name}" deleted by user named "{current_user["name"]}"')

    return Response(204, "success", "Signature successfully deleted")


def signature_updation(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('unique_name') or not payload.get('new'):
        return Response(400, "error", message="Incomplete information")

    unique_name = payload.get('unique_name')
    new = payload.get('new')

    signatures_collection = database.get_collection(collections[Signature])
    signature = signatures_collection.find_one({ 'unique_name': unique_name })

    if not signature:
        return Response(404, "error", message="Signature not found")
    
    for key in new.keys():
        if key not in signature.keys():
            return Response(400, "error", message=f"Invalid attribute to update: {key}")
        
    if new.get('unique_name'):
        return Response(400, "error", message=f"Invalid attribute to update: unique_name")
        
    if new.get('sender_picture'):
        # Process and save picture
        sender_picture = new.get('sender_picture')
        restrictions = Signature.get_image_restrictions()
        img_info = get_image_info(sender_picture)

        if img_info.get('error'):
            return Response(400, "error", message="Invalid image")

        if img_info['format'] not in restrictions['allowed_formats']:
            return Response(400, "error", message=f"Invalid image format: {img_info['format']}")
        
        if img_info['width'] < restrictions['width'][0] or img_info['width'] > restrictions['width'][1] or img_info['height'] < restrictions['height'][0] or img_info['height'] > restrictions['height'][1]:
            return Response(400, "error", message="Invalid image dimensions")
        
        save_info = save_image(sender_picture)
        if save_info.get('error'):
            return Response(500, "error", message="Error while saving image")
        
        sender_picture = save_info['filename']
        new['sender_picture'] = sender_picture
        delete_image(signature['sender_picture'])
        
    updated = signatures_collection.update_one({ 'unique_name': unique_name }, { '$set': new })

    if updated.acknowledged:
        logger.debug(f'signature named "{unique_name}" updated by user named "{current_user["name"]}", updated: {new}')

        return Response(200, "success", "Signature updated successfully")

    return Response(500, "error", "Signature updation failed")
    

def all_signatures(database: Database) -> Response:

    signatures_collection = database.get_collection(collections[Signature])
    signatures = list(signatures_collection.find())
    for signature in signatures:
        signature['_id'] = str(signature['_id'])

    return Response(200, "success", payload=signatures)
    