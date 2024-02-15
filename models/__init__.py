from .user import User
from .signature import Signature
from .product import Product, ProductType
from .industry import Industry
from .email_template import EmailTemplate
from .comparison import Comparison
from .company import Company
from .commercial import Commercial, PaymentTerms, ProposalType


collections = {
    User: "users",
    Signature: "signatures",
    ProductType: "product_types",
    PaymentTerms: "payment_terms",
    ProposalType: "proposal_type",
    Product: "products",
    Industry: "industries",
    EmailTemplate: "email_templates",
    Comparison: "comparisons",
    Company: "companies",
    Commercial: "commercials"
}
