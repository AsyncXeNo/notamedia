from bson import ObjectId

from models.price import Price


class ProductType:
    def __init__(self, name: str) -> None:
        self.name = name

    def to_dict(self):
        return {
            "name": self.name
        }
    

class Product:
    def __init__(self, unique_name: str, product_type: dict, item_description: str, particulars: str, 
                 default_quantity: int, fixed_quantity: bool, unit: str,
                 base_price: Price, implementation_fee: Price, 
                 default_vendor_discount: float, description_left: str, description_right: str):
        self.unique_name = unique_name
        self.product_type = product_type
        self.item_description = item_description
        self.particulars = particulars
        self.default_quantity = default_quantity
        self.fixed_quantity = fixed_quantity
        self.unit = unit
        self.base_price = base_price
        self.implementation_fee = implementation_fee
        self.default_vendor_discount = default_vendor_discount
        self.description_left = description_left
        self.description_right = description_right
    
    def to_dict(self):
        return {
            "unique_name": self.unique_name,
            "product_type": self.product_type,
            "item_description": self.item_description,
            "particulars": self.particulars,
            "default_quantity": self.default_quantity,
            "fixed_quantity": self.fixed_quantity,
            "unit": self.unit,
            "base_price": self.base_price.to_dict(),
            "implementation_fee": self.implementation_fee.to_dict(),
            "default_vendor_discount": self.default_vendor_discount,
            "description_left": self.description_left,
            "description_right": self.description_right
        }
