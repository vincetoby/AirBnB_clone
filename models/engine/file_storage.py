#!/usr/bin/python3
'''File Storage'''
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State
from models.city import City


class FileStorage:
    '''serializes instances to a JSON file and
        deserializes JSON file to instances'''

    __file_path = 'file.json'
    __objects = {}
    class_dict = {"BaseModel": BaseModel, "User": User, "Place": Place,
                  "Amenity": Amenity, "City": City, "Review": Review,
                  "State": State}

    def all(self):
        '''Returns the dictionary __object'''
        return self.__objects

    def new(self, obj):
        '''Adds new obj to existing dictionary of instances'''
        if obj:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        ''' serializes/saves __objects to the JSON file'''
        madict = {}

        for key, obj in self.__objects.items():
            madict[key] = obj.to_dict()
        with open(self.__file_path, 'w') as fi:
            json.dump(madict, fi)

    def reload(self):
        '''deserializes json file | converts obj dicts back to instances'''
        try:
            with open(self.__file_path, 'r') as f:
                new_objkt = json.load(f)
            for key, v in new_objkt.items():
                obj = self.class_dict[v['__class__']](**v)
                self.__objects[key] = obj
        except FileNotFoundError:
            pass
