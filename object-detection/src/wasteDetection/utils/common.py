import os
import sys
import yaml
import base64


from wasteDetection.logger import logging
from wasteDetection.exception import AppException

def read_yaml(file_path: str)->dict:
    """
    Read yaml file
    :param file_path: file path
    :return: yaml data
    """
    try:
        with open(file_path, "r") as file:
            logging.info(f"Reading yaml file from path {file_path}")
            return yaml.safe_load(file)
    except Exception as e:
        error_message = "Error occurred while reading yaml file"
        logging.error(error_message, exc_info=True)
        raise AppException(error_message, error_detail=sys.exc_info())
    
def write_yaml_file(file_path:str, content:object, replace : bool = False):
    """
    Write yaml file
    :param file_path: file path
    :param content: content to write in yaml file
    :param replace: replace file if already exists
    """
    try:
        if os.path.exists(file_path) and replace:
            logging.info(f"File already exists at path {file_path}. Removing file")
            os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)
            logging.info(f"Writing yaml file at path")
    except Exception as e:
        error_message = "Error occurred while writing yaml file"
        logging.error(error_message, exc_info=True)
        raise AppException(error_message, error_detail=sys.exc_info())
    

def encode_image(image_path:str):
    """
    Encode image to base64
    :param image_path: image path
    :return: base64 encoded image
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read())
    except Exception as e:
        error_message = "Error occurred while encoding image to base64"
        logging.error(error_message, exc_info=True)
        raise AppException(error_message, error_detail=sys.exc_info())
    

def decode_image(encoded_image:str, image_path:str):
    """
    Decode base64 image
    :param encoded_image: base64 encoded image
    :param image_path: image path to save decoded image
    """
    try:
        with open(image_path, "wb") as image_file:
            image_file.write(base64.b64decode(encoded_image))
    except Exception as e:
        error_message = "Error occurred while decoding image from base64"
        logging.error(error_message, exc_info=True)
        raise AppException(error_message, error_detail=sys.exc_info())