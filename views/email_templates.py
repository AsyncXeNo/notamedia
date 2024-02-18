from loguru import logger
from pymongo.database import Database

from models import collections
from models.email_template import EmailTemplate
from views.response import Response


def email_template_creation(current_user: dict, database: Database, payload: dict) -> Response:
    
    try:
        type_ = payload['type']
        subject = payload['subject']
        title = payload['title']
        subtitle = payload['subtitle']
        preview = payload['preview']
        
        above_email_body = payload['above_email_body']
        upper = payload['upper']
        middle_text = payload['middle_text']
        lower = payload['lower']
        below_email_body = payload['below_email_body']

        attachments = payload['attachments']
        additional_data = payload['additional_data']
        payment_url = payload['payment_url']
    except KeyError:
        return Response(400, 'error', message='Incomplete information')

    if not type_:
        return Response(400, "error", message="Incomplete information")
    
    email_templates_collection = database.get_collection(collections.get(EmailTemplate))

    existing_template = email_templates_collection.find_one({ 'type': type_ })
    if existing_template:
        return Response(409, 'error', message='Template already exists')

    template = EmailTemplate(
        type_,
        subject,
        title,
        subtitle,
        preview,
        above_email_body,
        upper,
        middle_text,
        lower,
        below_email_body,
        attachments,
        additional_data,
        payment_url
    )
    
    inserted = email_templates_collection.insert_one(template.to_dict())

    if inserted.acknowledged:
        logger.debug(f'new email template created by user named "{current_user["name"]}"')
        return Response(201, 'success', payload={
                            'type': type_
                        })
    
    return Response(500, 'error', 'Something went wrong')


def email_template_updation(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('type') or not payload.get('new'):
        return Response(400, 'error', message='Incomplete information')

    type_ = payload['type']
    new = payload['new']
    
    if new.get('_id'):
        return Response(400, "error", message=f"Invalid attribute to update: _id ")

    email_templates_collection = database.get_collection(collections.get(EmailTemplate))

    existing_template = email_templates_collection.find_one( {'type': type_} )
    if not existing_template:
        return Response(404, 'error', message='Template does not exist')
    
    for key in new.keys():
        if key not in existing_template.keys():
            return Response(400, "error", message=f"Invalid attribute to update: {key} ")
        
    updated = email_templates_collection.update_one({ 'type': type_ }, { '$set': new })

    if updated.acknowledged:
        logger.debug(f'email template ("{type_}") was updated by user named "{current_user["name"]}"')
        return Response(200, 'success', message='Template successfully updated')
    
    return Response(500, 'error', 'Something went wrong')
        

def email_template_deletion(current_user: dict, database: Database, payload: dict) -> Response:

    if not payload.get('type'):
        return Response(400, 'error', message='Incomplete information')
    
    type_ = payload['type']
    
    email_templates_collection = database.get_collection(collections.get(EmailTemplate))

    existing_template = email_templates_collection.find_one( {'type': type_} )
    if not existing_template:
        return Response(404, 'error', message='Template does not exist')
    
    email_templates_collection.delete_one({ 'type': type_ })
    logger.warning(f'Email template ("{type_}") has been deleted by user named "{current_user["name"]}"')

    return Response(200, 'success', 'Template successfully deleted')


def email_template_existing(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('type'):
        return Response(400, 'error', message='Incomplete information')
    
    type_ = payload['type']
    
    email_templates_collection = database.get_collection(collections.get(EmailTemplate))

    existing_template = email_templates_collection.find_one( {'type': type_} )
    if not existing_template:
        return Response(404, 'error', message='Template does not exist')

    existing_template['_id'] = str(existing_template['_id'])
    
    return Response(200, 'success', payload=existing_template)


def all_email_templates(database: Database) -> Response:
    
    email_templates_collection = database.get_collection(collections.get(EmailTemplate))
    templates = list(email_templates_collection.find())

    for template in templates:
        template['_id'] = str(template['_id'])

    return Response(200, 'success', payload=templates)