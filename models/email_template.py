from enum import Enum


def Placeholder(enum):
    COMPANY_NAME = 1
    CLIENT_NAME = 2


class EmailTemplate:
    def __init__(self, type: str, subject: tuple, title: tuple, subtitle: tuple,
                 preview: tuple, email_heading: tuple, email_para_1: tuple,
                 email_para_2: tuple, email_para_3: tuple, email_para_4: tuple,
                 middle_text: str, email_para_5: tuple, email_para_6: tuple,
                 email_para_7: tuple, email_para_8: tuple, attachments: list,
                 additional_data: str, payment_url: str, invoice_id: str,
                 above_email_body: str, below_email_body: str):
        self.type = type
        self.subject = subject
        self.title = title
        self.subtitle = subtitle
        self.preview = preview
        self.email_heading = email_heading
        self.email_para_1 = email_para_1
        self.email_para_2 = email_para_2
        self.email_para_3 = email_para_3
        self.email_para_4 = email_para_4
        self.middle_text = middle_text
        self.email_para_5 = email_para_5
        self.email_para_6 = email_para_6
        self.email_para_7 = email_para_7
        self.email_para_8 = email_para_8
        self.attachments = attachments
        self.additional_data = additional_data
        self.payment_url = payment_url
        self.invoice_id = invoice_id
        self.above_email_body = above_email_body
        self.below_email_body = below_email_body
    
    def to_dict(self):
        return {
            "type": self.type,
            "subject": self.subject,
            "title": self.title,
            "subtitle": self.subtitle,
            "preview": self.preview,
            "email_heading": self.email_heading,
            "email_para_1": self.email_para_1,
            "email_para_2": self.email_para_2,
            "email_para_3": self.email_para_3,
            "email_para_4": self.email_para_4,
            "middle_text": self.middle_text,
            "email_para_5": self.email_para_5,
            "email_para_6": self.email_para_6,
            "email_para_7": self.email_para_7,
            "email_para_8": self.email_para_8,
            "attachments": self.attachments,
            "additional_data": self.additional_data,
            "payment_url": self.payment_url,
            "invoice_id": self.invoice_id,
            "above_email_body": self.above_email_body,
            "below_email_body": self.below_email_body
        }
