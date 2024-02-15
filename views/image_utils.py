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


def get_image(filename):
    try:
        with open(filename, "rb") as f:
            image_bytes = f.read()
            encoded_image = base64.b64encode(image_bytes).decode("utf-8")
            return { "data": encoded_image }
    except Exception as e:
            return { "error": str(e) }


def delete_image(filename) -> bool:
    try:
        os.remove(filename)
        return True
    except:
        return False