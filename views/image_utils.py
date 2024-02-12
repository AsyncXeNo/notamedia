import os
import uuid
import base64
from PIL import Image
from io import BytesIO


def get_image_info(encoded_image):
    try:
        decoded_image = base64.b64decode(encoded_image)
        img = Image.open(BytesIO(decoded_image))
        width, height = img.size
        img_format = img.format.lower()
        return {
            "width": width,
            "height": height,
            "format": img_format
        }
    except Exception as e:
        return {
            "error": str(e)
        }
    

def save_image(encoded_image):
    try:
        decoded_image = base64.b64decode(encoded_image)
        filename = "data/images/" + str(uuid.uuid4()) + ".jpg"

        with open(filename, "wb") as f:
            f.write(decoded_image)

        return { "filename": filename }
    
    except Exception as e:
        return { "error": str(e) }
    

def delete_image(filename) -> bool:
    try:
        os.remove(filename)
        return True
    except:
        return False