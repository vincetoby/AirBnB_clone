#!/usr/bin/python3
""" defines a class Review """
from models.base_model import BaseModel


class Review(BaseModel):
    """ a class that inherits from BaseModel """
    place_id = ""
    user_id = ""
    text = ""
