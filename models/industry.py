class Industry:
    def __init__(self, name: str, images: list):
        self.name = name
        self.images = images
    
    def to_dict(self):
        return {
            "name": self.name,
            "images": self.images[:5]  # Limiting to 5 images for simplicity
        }