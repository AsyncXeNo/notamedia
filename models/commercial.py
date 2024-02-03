from bson import ObjectId


class PaymentTerms:
    def __init__(self, name: str, terms: str):
        self.name = name
        self.terms = terms
    
    def to_dict(self):
        return {
            "name": self.name,
            "terms": self.terms
        }


class ProposalType:
    def __init__(self, name: str):
        self.name = name
    
    def to_dict(self):
        return {
            "name": self.name
        }


class Commercial:
    def __init__(self, company_id: ObjectId, proposal_title: str, proposal_currency: str,
                 signature_id: ObjectId, payment_terms_id: ObjectId, proposal_type_id: ObjectId,
                 email_template_id: ObjectId, product_list: list[ObjectId],
                 comparisons: list[ObjectId]):
        self.company_id = company_id
        self.proposal_title = proposal_title
        self.proposal_currency = proposal_currency
        self.signature_id = signature_id
        self.payment_terms_id = payment_terms_id
        self.proposal_type_id = proposal_type_id
        self.email_template_id = email_template_id
        self.product_list = product_list
        self.comparisons = comparisons
    
    def to_dict(self):
        return {
            "company_id": str(self.company_id),  # Convert ObjectId to string for JSON serialization
            "proposal_title": self.proposal_title,
            "proposal_currency": self.proposal_currency,
            "signature_id": str(self.signature_id),
            "payment_terms_id": str(self.payment_terms_id),
            "proposal_type_id": str(self.proposal_type_id),
            "email_template_id": str(self.email_template_id),
            "product_list": [str(product_id) for product_id in self.product_list],  # Convert ObjectId list to strings
            "comparisons": [str(comparison_id) for comparison_id in self.comparisons]
        }
