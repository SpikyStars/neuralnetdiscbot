import requests
from PIL import Image, UnidentifiedImageError


def read_image(url):
    try:
        response = requests.get(url, stream=True)
        image = Image.open(response.raw).convert("RGB")
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        raise InputException("The link you sent doesn't appear to be a valid link!")
    except UnidentifiedImageError:
        raise InputException("The link you sent isn't a direct link to a supported image format!")
    return image


class ProcessingException(Exception):
    pass


class InputException(ProcessingException):
    def __init__(self, message):
        self.message = message
