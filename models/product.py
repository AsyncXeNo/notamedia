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
    def __init__(self, product_type_id: ObjectId, item_description: str, particulars: str, 
                 default_quantity: int, fixed_quantity: bool, unit_count: float,
                 base_price: Price, implementation_fee: Price, 
                 default_vendor_discount: int, description_left: str, description_right: str):
        self.product_type_id = product_type_id
        self.item_description = item_description
        self.particulars = particulars
        self.default_quantity = default_quantity
        self.fixed_quantity = fixed_quantity
        self.unit_count = unit_count
        self.base_price = base_price
        self.implementation_fee = implementation_fee
        self.default_vendor_discount = default_vendor_discount
        self.description_left = description_left
        self.description_right = description_right
    
    def to_dict(self):
        return {
            "product_type_id": str(self.product_type_id),
            "item_description": self.item_description,
            "particulars": self.particulars,
            "default_quantity": self.default_quantity,
            "fixed_quantity": self.fixed_quantity,
            "unit_count": self.unit_count,
            "base_price": self.base_price.to_dict(),
            "implementation_fee": self.implementation_fee.to_dict(),
            "default_vendor_discount": self.default_vendor_discount,
            "description_left": self.description_left,
            "description_right": self.description_right
        }
