from enum import Enum
from bson import ObjectId
from datetime import datetime


class Person():
    def __init__(self, name: str, designation: str, phone: str, email: str) -> None:
        self.name = name
        self.designation = designation
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            'name': self.name,
            'designation': self.designation,
            'phone': self.phone,
            'email': self.email
        }


class ClientLocationForTax(Enum):

    INSIDE_DELHI = 1
    OUTSIDE_DELHI = 2
    FOREIGN = 3
    NO_TAX = 4


class PlanType:
    def __init__(self, name: str):
        self.name = name

    def to_dict(self):
        return {
            'name': self.name,
        }


class Company:
    def __init__(self, 
                 name: str, 
                 logo: str, 
                 people: list[dict],
                 company_websites: list, 
                 state: str, 
                 client_location_for_tax: int, 
                 start_date: int, 
                 full_address_with_pin: str,
                 gst: str, 
                 industry: dict, 
                 plan_type: str, 
                 bitrix_url: str, 
                 license_extension: str):
        self.name = name
        self.logo = logo  # Assuming logo is a file path or reference
        self.people = people
        self.company_websites = company_websites[:3]  # Limiting to 3 websites for simplicity
        self.state = state
        self.client_location_for_tax = client_location_for_tax
        self.start_date = start_date
        self.full_address_with_pin = full_address_with_pin
        self.gst = gst
        self.industry = industry
        self.plan_type = plan_type
        self.bitrix_url = bitrix_url
        self.license_extension = license_extension

    def get_image_restrictions():
        return {
            'allowed_formats': ['jpg', 'jpeg', 'png'],
            'width': (0, 10000),
            'height': (0, 10000)
        }
    
    def to_dict(self):
        return {
            "name": self.name,
            "logo": self.logo,
            "people": self.people,
            "company_websites": self.company_websites,
            "state": self.state,
            "client_location_for_tax": self.client_location_for_tax,
            "start_date": self.start_date,
            "full_address_with_pin": self.full_address_with_pin,
            "gst": self.gst,
            "industry": self.industry,
            "plan_type": self.plan_type,
            "bitrix_url": self.bitrix_url,
            "license_extension": self.license_extension
        }
