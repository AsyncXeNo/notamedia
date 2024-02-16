class Industry:
    def __init__(self, name: str, images: list):
        self.name = name
        self.images = images

    def get_image_restrictions():
        return {
            'allowed_formats': ['jpg', 'jpeg', 'png'],
            'width': (0, 10000),
            'height': (0, 10000)
        }
    
    def to_dict(self):
        return {
            "name": self.name,
            "images": self.images  # Limiting to 5 images for simplicity
        }