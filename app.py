import config as _

import json
import logging
import traceback
from flask import Flask, request
from flask_cors import CORS, cross_origin
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from loguru import logger

from models.user import UserType
from views.users import require_user_type, user_login, user_registration, create_new_client_user, user_deletion, user_updation, user_existing, all_users
from views.products import product_type_creation, product_type_deletion, all_product_types, product_creation, product_updation, product_deletion, product_existing, all_products
from views.signatures import signature_creation, signature_deletion, signature_updation, signature_existing, all_signatures
from views.comparisons import comparison_creation, comparison_updation, comparison_deletion, comparison_existing, all_comparisons
from views.email_templates import email_template_creation, email_template_updation, email_template_deletion, email_template_existing, all_email_templates
from views.industries import industry_creation, industry_updation, industry_deletion, industry_existing, all_industries
from views.plan_types import plan_type_creation, plan_type_deletion, all_plan_types
from views.companies import company_creation, company_updation, company_deletion, company_existing, all_companies
from views.proposal_types import proposal_type_creation, proposal_type_deletion, all_proposal_types
from views.payment_terms import payment_terms_creation, payment_terms_updation, payment_terms_deletion, payment_terms_existing, all_payment_terms
from views.commercials import commercial_creation, commercial_updation, commercial_deletion, commercial_existing, all_commercials
from views.response import Response
from mongo import setup


HOST = 'localhost'
PORT = 12345

client, database = setup()
client: MongoClient
database: Database

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True


# Error Handling

@app.errorhandler(500)
def internal_server_error(e):

    lines = traceback.format_exc().split('\n')
    while True:
        try: lines.remove('')
        except: break

    error = lines[-1]
    
    logger.error(error)
    return Response(500, 'error', payload={'error': error}, message='Something went wrong').to_response()


"""
USER ROUTES
"""

@app.route('/users/login', methods=['POST'])
@cross_origin()
def login():

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return user_login(database, payload)


@app.route('/users/new', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def register_user(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()
    
    payload = json.loads(request.data)
    return user_registration(current_user, database, payload)


@app.route('/users/delete', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_user(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return user_deletion(current_user, database, payload)


@app.route('/users/update', methods=['PUT'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def update_user(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()
    
    payload = json.loads(request.data)
    return user_updation(current_user, database, payload)


@app.route('/users/me', methods=['GET'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN, UserType.WORKER, UserType.CLIENT)
def get_user(current_user):

    del(current_user['hashed_password'])
    current_user['_id'] = str(current_user.get('_id'))
    
    return Response(200, 'success', payload=current_user).to_response()


@app.route('/users/existing', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def get_existing_user(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return user_existing(current_user, database, payload)


@app.route('/users', methods=['GET'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def get_users(current_user):

    return all_users(database)


"""
PRODUCT TYPE ROUTES
"""    

@app.route('/products/types/new', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def new_product_type(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return product_type_creation(current_user, database, payload)


@app.route('/products/types/delete', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_product_type(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return product_type_deletion(current_user, database, payload)


@app.route('/products/types', methods=['GET'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_product_types(current_user):

    return all_product_types(database)


"""
PRODUCT ROUTES
"""

@app.route('/products/new', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def new_product(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return product_creation(current_user, database, payload).to_response()


@app.route('/products/update', methods=['PUT'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def update_product(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return product_updation(current_user, database, payload).to_response()
    

@app.route('/products/delete', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_product(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return product_deletion(current_user, database, payload).to_response()


@app.route('/products/existing', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_existing_product(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return product_existing(current_user, database, payload).to_response()


@app.route('/products', methods=['GET'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_products(current_user):

    return all_products(database).to_response()
    

"""
SIGNATURE ROUTES
"""

@app.route('/signatures/new', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def new_signature(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()
    
    payload = json.loads(request.data)
    return signature_creation(current_user, database, payload).to_response()


@app.route('/signatures/delete', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_signature(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return signature_deletion(current_user, database, payload).to_response()


@app.route('/signatures/update', methods=['PUT'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def update_signature(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return signature_updation(current_user, database, payload).to_response()


@app.route('/signatures/existing', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_existing_signature(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return signature_existing(current_user, database, payload).to_response()


@app.route('/signatures', methods=['GET'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_signatures(current_user):

    return all_signatures(database).to_response()


"""
EMAIL TEMPLATES
"""


@app.route('/emails/new', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def new_email_template(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return email_template_creation(current_user, database, payload).to_response()


@app.route('/emails/update', methods=['PUT'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def update_email_template(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return email_template_updation(current_user, database, payload).to_response()


@app.route('/emails/delete', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_email_template(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return email_template_deletion(current_user, database, payload).to_response()


@app.route('/emails/existing', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def get_existing_email_template(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return email_template_existing(current_user, database, payload).to_response()
    

@app.route('/emails', methods=['GET'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_email_templates(current_user):

    return all_email_templates(database).to_response()


"""
COMPARISON ROUTES
"""


@app.route('/comparisons/new', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def new_comparison(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return comparison_creation(current_user, database, payload).to_response()


@app.route('/comparisons/update', methods=['PUT'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def update_comparison(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return comparison_updation(current_user, database, payload).to_response()


@app.route('/comparisons/delete', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_comparison(current_user):
    
    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return comparison_deletion(current_user, database, payload).to_response()


@app.route('/comparisons/existing', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_existing_comparison(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return comparison_existing(current_user, database, payload).to_response()


@app.route('/comparisons', methods=['GET'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_comparisons(current_user):

    return all_comparisons(database).to_response()


"""
INDUSTRY ROUTES
"""


@app.route('/industries/new', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def create_industry(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return industry_creation(current_user, database, payload).to_response()


@app.route('/industries/update', methods=['PUT'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def update_industry(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return industry_updation(current_user, database, payload).to_response()


@app.route('/industries/delete', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_industry(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return industry_deletion(current_user, database, payload).to_response()


@app.route('/industries/existing', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_existing_industry(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return industry_existing(current_user, database, payload).to_response()


@app.route('/industries', methods=['GET'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_industries(current_user):

    return all_industries(database).to_response()


"""
PLAN TYPE ROUTES
"""


@app.route('/plan_types/new', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def create_plan_type(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return plan_type_creation(current_user, database, payload).to_response()



@app.route('/plan_types/delete', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_plan_type(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return plan_type_deletion(current_user, database, payload).to_response()


@app.route('/plan_types', methods=['GET'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_plan_types(current_user):

    return all_plan_types(database).to_response()


"""
COMPANY ROUTES
"""

@app.route('/companies/new', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def create_company(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return company_creation(current_user, database, payload).to_response()


@app.route('/companies/update', methods=['PUT'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def update_company(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return company_updation(current_user, database, payload).to_response()


@app.route('/companies/delete', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_company(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return company_deletion(current_user, database, payload).to_response()


@app.route('/companies/existing', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_existing_company(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return company_existing(current_user, database, payload).to_response()


@app.route('/companies', methods=['GET'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_companies(current_user):

    return all_companies(database).to_response()
    

"""
PROPOSAL TYPE ROUTES
"""


@app.route('/proposal_types/new', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def create_proposal_type(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return proposal_type_creation(current_user, database, payload).to_response()



@app.route('/proposal_types/delete', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_proposal_type(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return proposal_type_deletion(current_user, database, payload).to_response()


@app.route('/proposal_types', methods=['GET'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_proposal_types(current_user):

    return all_proposal_types(database).to_response()


"""
PAYMENT TERMS
"""


@app.route('/payment_terms/new', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def create_payment_terms(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return payment_terms_creation(current_user, database, payload).to_response()


@app.route('/payment_terms/update', methods=['PUT'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def update_payment_terms(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return payment_terms_updation(current_user, database, payload).to_response()


@app.route('/payment_terms/delete', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_payment_terms(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return payment_terms_deletion(current_user, database, payload).to_response()


@app.route('/payment_terms/existing', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_existing_payment_terms(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return payment_terms_existing(current_user, database, payload).to_response()


@app.route('/payment_terms', methods=['GET'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_payment_terms(current_user):

    return all_payment_terms(database).to_response()


"""
COMMERCIAL ROUTES
"""


@app.route('/commercials/new', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def create_commercial(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return commercial_creation(current_user, database, payload).to_response()


@app.route('/commercials/update', methods=['PUT'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def update_commercial(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return commercial_updation(current_user, database, payload).to_response()


@app.route('/commercials/delete', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.SUPER_ADMIN)
def delete_commercial(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return commercial_deletion(current_user, database, payload).to_response()


@app.route('/commercials/existing', methods=['POST'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_existing_commercial(current_user):

    if not request.data: return Response(400, "error", message="Incomplete information").to_response()

    payload = json.loads(request.data)
    return commercial_existing(current_user, database, payload).to_response()


@app.route('/commercials', methods=['GET'])
@cross_origin()
@require_user_type(database, UserType.WORKER, UserType.SUPER_ADMIN)
def get_commercials(current_user):

    return all_commercials(database).to_response()


if __name__ == '__main__':

    logger.info(f'starting server: {HOST}:{PORT}')
    
    app.run(
        host=HOST,
        port=PORT,
        debug=False
    )