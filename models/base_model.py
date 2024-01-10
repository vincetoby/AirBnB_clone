#!/usr/bin/python3
"""Class BaseModel"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """defines common attributes and methods for other classes"""
    formatofstr = "%Y-%m-%dT%H:%M:%S.%f"

    def __init__(self, *args, **kwargs):
        """the Constructor"""
        if kwargs:
            for kw, vw in kwargs.items():
                if kw == "created_at" or k == "updated_at":
                    setattr(self, kw, datetime.strptime(vw, self.formatofstr))
                elif kw != "__class__":
                    setattr(self, kw, vw)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """it returns [<class name>] (<self.id>) <self.__dict__>"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """it updates updated_at with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        a method that returns a dictionary containing all keys/values
        of __dict__ of the instance
        """
        dicto = {}
        dicto["__class__"] = self.__class__.__name__
        for kw, vw in self.__dict__.items():
            if isinstance(vw, (datetime, )):
                dicto[kw] = vw.isoformat()
            else:
                dicto[kw] = vw
        return dicto
