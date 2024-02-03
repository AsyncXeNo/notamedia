class Signature:
    def __init__(self, sender_full_name: str, sender_short_name: str, sender_designation: str,
                 sender_phone: str, sender_email: str, sender_company_website: str,
                 sender_picture: str, sender_company_name: str):
        self.sender_full_name = sender_full_name
        self.sender_short_name = sender_short_name
        self.sender_designation = sender_designation
        self.sender_phone = sender_phone
        self.sender_email = sender_email
        self.sender_company_website = sender_company_website
        self.sender_picture = sender_picture
        self.sender_company_name = sender_company_name
    
    def to_dict(self):
        return {
            "sender_full_name": self.sender_full_name,
            "sender_short_name": self.sender_short_name,
            "sender_designation": self.sender_designation,
            "sender_phone": self.sender_phone,
            "sender_email": self.sender_email,
            "sender_company_website": self.sender_company_website,
            "sender_picture": self.sender_picture,
            "sender_company_name": self.sender_company_name
        }
