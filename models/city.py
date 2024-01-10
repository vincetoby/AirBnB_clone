#!/usr/bin/python3
""" defines a class City """
from models.base_model import BaseModel


class City(BaseModel):
    """ a class that inherits from BaseModel """
    state_id = ""
    name = ""
