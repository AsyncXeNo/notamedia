from loguru import logger
from pymongo.database import Database

from models import collections
from models.industry import Industry
from views.response import Response


def industry_creation(current_user: dict, database: Database, payload: dict) -> Response:
    pass


def industry_updation(current_user: dict, database: Database, payload: dict) -> Response:
    pass


def industry_deletion(current_user: dict, database: Database, payload: dict) -> Response:
    pass


def industry_existing(current_user: dict, database: Database, payload: dict) -> Response:
    pass


def all_industries(database: Database) -> Response:
    pass