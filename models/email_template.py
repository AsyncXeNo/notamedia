from enum import Enum


def Placeholder(enum):
    COMPANY_NAME = 1
    CLIENT_NAME = 2


class EmailTemplate:
    def __init__(self, type: str, subject: list, title: list, subtitle: list,
                 preview: list, above_email_body: str, upper: list[tuple[str, list]],
                 middle_text: str, lower: list[tuple[str, list]], below_email_body: str,
                 attachments: list,
                 additional_data: str, payment_url: str):
        self.type = type
        self.subject = subject
        self.title = title
        self.subtitle = subtitle
        self.preview = preview
        
        self.above_email_body = above_email_body
        self.upper = upper
        self.middle_text = middle_text
        self.lower = lower
        self.below_email_body = below_email_body

        self.attachments = attachments
        self.additional_data = additional_data
        self.payment_url = payment_url
    
    def to_dict(self):
        return {
            "type": self.type,
            "subject": self.subject,
            "title": self.title,
            "subtitle": self.subtitle,
            "preview": self.preview,
            
            "above_email_body": self.above_email_body,
            "upper": self.upper,
            "middle_text": self.middle_text,
            "lower": self.lower,
            "below_email_body": self.below_email_body,

            "attachments": self.attachments,
            "additional_data": self.additional_data,
            "payment_url": self.payment_url
        }
