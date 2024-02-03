from bson import ObjectId
from datetime import datetime


class Company:
    def __init__(self, name: str, logo: str, people_id: ObjectId, company_websites: list, 
                 state: str, client_location_for_tax: str, start_date: datetime, 
                 full_address_with_pin: str, industry_id: ObjectId, plan_type: str, 
                 bitrix_url: str, license_extension: str):
        self.name = name
        self.logo = logo  # Assuming logo is a file path or reference
        self.people_id = people_id
        self.company_websites = company_websites[:3]  # Limiting to 3 websites for simplicity
        self.state = state
        self.client_location_for_tax = client_location_for_tax
        self.start_date = start_date
        self.full_address_with_pin = full_address_with_pin
        self.industry_id = industry_id
        self.plan_type = plan_type
        self.bitrix_url = bitrix_url
        self.license_extension = license_extension
    
    def to_dict(self):
        return {
            "name": self.name,
            "logo": self.logo,
            "people_id": str(self.people_id),  # Convert ObjectId to string for JSON serialization
            "company_websites": self.company_websites,
            "state": self.state,
            "client_location_for_tax": self.client_location_for_tax,
            "start_date": self.start_date,
            "full_address_with_pin": self.full_address_with_pin,
            "industry_id": str(self.industry_id),  # Convert ObjectId to string for JSON serialization
            "plan_type": self.plan_type,
            "bitrix_url": self.bitrix_url,
            "license_extension": self.license_extension
        }
