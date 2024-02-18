from bson import ObjectId

from loguru import logger
from pymongo.database import Database

from views.response import Response
from models import collections
from models.commercial import Commercial, PaymentTerms, ProposalType
from models.company import Company
from models.signature import Signature
from models.email_template import EmailTemplate
from models.comparison import Comparison


def commercial_creation(current_user: dict, database: Database, payload: dict) -> Response:
    
    try:
        title = payload['title']
        currency = payload['currency']
        company_id = payload['company_id']
        signature_id = payload['signature_id']
        payment_terms_id = payload['payment_terms_id']
        proposal_type_id = payload['proposal_type_id']
        email_template_id = payload['email_template_id']
        product_list = payload['product_list']
        comparisons = payload['comparisons']
    except KeyError:
        return Response(400, 'error', 'Incomplete information')
    
    if not title or not currency or not company_id or not signature_id or not payment_terms_id or not proposal_type_id or not email_template_id or product_list is None or comparisons is None:
        return Response(400, 'error', 'Incomplete information')
    
    commercials_collection = database.get_collection(collections.get(Commercial))
    
    existing_commercial = commercials_collection.find_one({ 'title': title })
    if existing_commercial:
        return Response(400, 'error', 'Commercial already exists')
    
    companies_collection = database.get_collection(collections.get(Company))
    signatures_collection = database.get_collection(collections.get(Signature))
    payment_terms_collection = database.get_collection(collections.get(PaymentTerms))
    proposal_types_collection = database.get_collection(collections.get(ProposalType))
    email_templates_collection = database.get_collection(collections.get(EmailTemplate))
    comparisons_collection = database.get_collection(collections.get(Comparison))

    if currency not in ['inr', 'usd', 'aed', 'eur', 'gbp']:
        return Response(400, 'error', 'Invalid currency')
    
    company = companies_collection.find_one({ '_id': ObjectId(company_id) })
    if not company:
        return Response(404, 'error', 'Company not found')
    
    signature = signatures_collection.find_one({ '_id': ObjectId(signature_id) })
    if not signature:
        return Response(404, 'error', 'Signature not found')

    payment_terms = payment_terms_collection.find_one({ '_id': ObjectId(payment_terms_id) })
    if not payment_terms:
        return Response(404, 'error', 'Payment terms not found')
    
    proposal_type = proposal_types_collection.find_one({ '_id': ObjectId(proposal_type_id) })
    if not proposal_type:
        return Response(404, 'error', 'Proposal type not found')
    
    email_template = email_templates_collection.find_one({ '_id': ObjectId(email_template_id) })
    if not email_template:
        return Response(404, 'error', 'Email template not found')
    
    for comparison in comparisons:
        entry = comparisons_collection.find_one({ '_id': ObjectId(comparison) })
        if not entry:
            return Response(404, 'error', f'Comparison not found: {comparison}')
        
    commercial = Commercial(
        company_id,
        title,
        currency,
        signature_id,
        payment_terms_id,
        proposal_type_id,
        email_template_id,
        product_list,
        comparisons
    )

    inserted = commercials_collection.insert_one(commercial.to_dict())
    if inserted.acknowledged:
        logger.debug(f'new commercial created ("{title}") by user named "{current_user["name"]}"')
        return Response(201, 'success', 'Commercial created successfully')
    
    return Response(500, 'error', 'Commercial creation failed')
    

def commercial_updation(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('title') or not payload.get('new'):
        return Response(400, 'error', 'Incomplete information')

    title = payload['title']
    new = payload['new']

    commercials_collection = database.get_collection(collections.get(Commercial))
    
    existing_commercial = commercials_collection.find_one({ 'title': title })
    if not existing_commercial:
        return Response(404, 'success', 'Commercial not found')
    
    for key in new.keys():
        if key not in existing_commercial.keys():
            return Response(400, "error", message=f"Invalid attribute to update: {key}")
        
    if new.get('_id'):
        return Response(400, "error", message=f"Invalid attribute to update: _id")
    
    if new.get('company_id'):
        companies_collection = database.get_collection(collections.get(Company))
        company = companies_collection.find_one({ '_id': ObjectId(new['company_id']) })
        if not company:
            return Response(404, 'error', 'Company not found')
        
    if new.get('signature_id'):
        signatures_collection = database.get_collection(collections.get(Signature))
        signature = signatures_collection.find_one({ '_id': ObjectId(new['signature_id']) })
        if not signature:
            return Response(404, 'error', 'Signature not found')
        
    if new.get('payment_terms_id'):
        payment_terms_collection = database.get_collection(collections.get(PaymentTerms))
        payment_terms = payment_terms_collection.find_one({ '_id': ObjectId(new['payment_terms_id']) })
        if not payment_terms:
            return Response(404, 'error', 'Payment terms not found')
        
    if new.get('proposal_type_id'):
        proposal_types_collection = database.get_collection(collections.get(ProposalType))
        proposal_type = proposal_types_collection.find_one({ '_id': ObjectId(new['proposal_type_id']) })
        if not proposal_type:
            return Response(404, 'error', 'Proposal type not found')
        
    if new.get('email_template_id'):
        email_templates_collection = database.get_collection(collections.get(EmailTemplate))
        email_template = email_templates_collection.find_one({ '_id': ObjectId(new['email_template_id']) })
        if not email_template:
            return Response(404, 'error', 'Email template not found')
        
    if new.get('comparisons'):
        comparisons = new['comparisons']
        comparisons_collection = database.get_collection(collections.get(Comparison))
        for comparison in comparisons:
            entry = comparisons_collection.find_one({ '_id': ObjectId(comparison) })
            if not entry:
                return Response(404, 'error', f'Comparison not found: {comparison}')
            
    updated = commercials_collection.update_one({ 'title': title }, { '$set': new })
    if updated.acknowledged:
        logger.debug(f'commercial titled "{title}" updated by user named "{current_user["name"]}"')
        return Response(200, 'success', 'Commercial successfully updated')

    return Response(500, 'error', 'Commercial updation failed')


def commercial_deletion(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('title'):
        return Response(400, 'error', 'Incomplete information')
    
    title = payload['title']

    commercials_collection = database.get_collection(collections.get(Commercial))
    
    existing_commercial = commercials_collection.find_one({ 'title': title })
    if not existing_commercial:
        return Response(404, 'success', 'Commercial not found')
    
    commercials_collection.delete_one({ 'title': title })
    logger.warning(f'commercial titled "{title}" deleted by user named "{current_user["name"]}"')

    return Response(200, 'success', 'Commercial deletion successful')


def commercial_existing(current_user: dict, database: Database, payload: dict) -> Response:
    
    if not payload.get('title'):
        return Response(400, 'error', 'Incomplete information')
    
    title = payload['title']

    commercials_collection = database.get_collection(collections.get(Commercial))
    
    existing_commercial = commercials_collection.find_one({ 'title': title })
    if not existing_commercial:
        return Response(404, 'success', 'Commercial not found')
    
    del(existing_commercial['_id'])

    return Response(200, 'success', payload=existing_commercial)


def all_commercials(database: Database) -> Response:
    
    commercials_collection = database.get_collection(collections.get(Commercial))
    commercials = list(commercials_collection.find())

    for commercial in commercials:
        commercial['_id'] = str(commercial['_id'])

    return Response(200, 'success', payload=commercials)