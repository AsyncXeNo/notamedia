from bson import ObjectId

from loguru import logger
from pymongo.database import Database

from views.response import Response
from views.image_utils import get_image_info, save_image, get_image, delete_image
from models import collections
from models.company import Company, Person, ClientLocationForTax


def company_creation(current_user: dict, database: Database, payload: dict) -> Response:
    
    try:
        name = payload['name']
        logo = payload['logo']
        people = payload['people']
        company_websites = payload['company_websites']
        state = payload['state']
        client_location_for_tax = payload['client_location_for_tax']
    except KeyError:
        return Response(400, 'error', 'Incomplete information')
    
    if not name or not logo or not people or not company_websites or not state or not client_location_for_tax:
        return Response(400, 'error', 'Incomplete information')

    start_date = payload.get('start_date')
    full_address_with_pin = payload.get('full_address_with_pin')
    gst = payload.get('gst')
    industry = payload.get('industry')
    plan_type = payload.get('plan_type')
    bitrix_url = payload.get('bitrix_url')
    license_extension = payload.get('license_extension')

    companies_collection = database.get_collection(collections.get(Company))

    existing_company = companies_collection.find_one({ 'name': name })
    if existing_company:
        return Response(400, 'error', 'Company already exists')

    new_people = []
    try:
        for person in people:
            p = Person(person['name'], person['designation'], person['phone'], person['email'])
            new_people.append(p.to_dict())
    except:
        return Response(400, 'error', 'Error while processing the "people" list')
    
    # Process and save logo
    restrictions = Company.get_image_restrictions()
    img_info = get_image_info(logo)

    if img_info.get('error'):
        return Response(400, "error", message="Invalid image")

    if img_info['format'] not in restrictions['allowed_formats']:
        return Response(400, "error", message=f"Invalid image format: {img_info['format']}")
    
    if img_info['width'] < restrictions['width'][0] or img_info['width'] > restrictions['width'][1] or img_info['height'] < restrictions['height'][0] or img_info['height'] > restrictions['height'][1]:
        return Response(400, "error", message="Invalid image dimensions")
    
    save_info = save_image(logo)
    if save_info.get('error'):
        return Response(500, "error", message="Error while saving image")
    
    logo = save_info.get('filename')

    if client_location_for_tax not in [1, 2, 3, 4]:
        return Response(400, 'error', message='Invalid client location for tax')
    
    company = Company(
        name,
        logo,
        people,
        company_websites,
        state,
        client_location_for_tax,
        start_date,
        full_address_with_pin,
        gst,
        industry,
        plan_type,
        bitrix_url,
        license_extension
    )

    inserted = companies_collection.insert_one(company.to_dict())

    if inserted.acknowledged:
        logger.debug(f'new company ("{name}") created by user named "{current_user["name"]}"')
        return Response(201, 'success', 'Company created successfully')
    
    return Response(500, 'success', 'Company creation failed')


def company_updation(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('name') or not payload.get('new'):
        return Response(400, 'error', 'Incomplete information')
    
    name = payload['name']
    new = payload['new']

    companies_collection = database.get_collection(collections.get(Company))

    existing_company = companies_collection.find_one({ 'name': name })
    if not existing_company:
        return Response(404, 'error', 'Company not found')
    
    for key in new.keys():
        if key not in existing_company.keys():
            return Response(400, "error", message=f"Invalid attribute to update: {key}")
        
    if new.get('_id'):
        return Response(400, "error", message=f"Invalid attribute to update: _id")
    
    if new.get('logo'):
        logo = new['logo']
        # Process and save logo
        restrictions = Company.get_image_restrictions()
        img_info = get_image_info(logo)

        if img_info.get('error'):
            return Response(400, "error", message="Invalid image")

        if img_info['format'] not in restrictions['allowed_formats']:
            return Response(400, "error", message=f"Invalid image format: {img_info['format']}")
        
        if img_info['width'] < restrictions['width'][0] or img_info['width'] > restrictions['width'][1] or img_info['height'] < restrictions['height'][0] or img_info['height'] > restrictions['height'][1]:
            return Response(400, "error", message="Invalid image dimensions")
        
        save_info = save_image(logo)
        if save_info.get('error'):
            return Response(500, "error", message="Error while saving image")
        
        logo = save_info.get('filename')
        new['logo'] = logo

    if new.get('client_location_for_tax'):
        if new['client_location_for_tax'] not in [1, 2, 3, 4]:
            return Response(400, 'error', message='Invalid client location for tax')
        
    updated = companies_collection.update_one({ 'name': name }, { '$set': new })

    if updated.acknowledged:
        logger.debug(f'company named {name} updated by user named "{current_user["name"]}"')

        if new.get('logo'):
            delete_image(existing_company['logo'])
        
        return Response(200, 'success', 'Company successfully updated')
    
    return Response(500, 'error', 'Company updation failed')


def company_deletion(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('name'):
        return Response(400, 'error', 'Incomplete information')
    
    name = payload['name']

    companies_collection = database.get_collection(collections.get(Company))

    existing_company = companies_collection.find_one({ 'name': name })
    if not existing_company:
        return Response(404, 'error', 'Company not found')
    
    companies_collection.delete_one({ 'name': name })
    logger.warning(f'company named {name} deleted by user named "{current_user["name"]}"')

    delete_image(existing_company['logo'])
    return Response(200, 'success', 'Company deleted successfully')


def company_existing(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('name'):
        return Response(400, 'error', 'Incomplete information')
    
    name = payload['name']

    companies_collection = database.get_collection(collections.get(Company))

    existing_company = companies_collection.find_one({ 'name': name })
    if not existing_company:
        return Response(404, 'error', 'Company not found')
    
    logo = existing_company['logo']

    image_encoded = get_image(logo)
    if image_encoded.get('error'):
        return Response(500, 'error', 'Error while reading logo image')
    
    existing_company['logo'] = image_encoded.get('data')
    existing_company['_id'] = str(existing_company['_id'])

    return Response(200, 'success', payload=existing_company)


def all_companies(database: Database) -> Response:
    
    companies_collection = database.get_collection(collections.get(Company))
    companies = list(companies_collection.find())

    companies_to_return = []

    for company in companies:
        companies_to_return.append({
            '_id': str(company['_id']),
            'name': company['name']
        })

    return Response(200, 'success', payload=companies_to_return)
    