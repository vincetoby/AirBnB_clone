#!/usr/bin/python3
"""defines a Class called User"""
from models.base_model import BaseModel


class User(BaseModel):
    """a class that inherits from BaseModel"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
