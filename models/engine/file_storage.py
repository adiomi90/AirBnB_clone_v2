#!/usr/bin/python3
"""The file storage  module for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            if type(cls) == str:
                cls = eval(cls)
            my_dict = {}
            for key, value in self.__objects.items():
                if type(value) == cls:
                    my_dict[key] = value
            return my_dict
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def get(self, cls, id):
        """retrieves specific object
        Args:
            cls: class of object as string
            id (str): id of object as string
        Return: found object or None
        """
        all_class = self.all(cls)
        for obj in all_class.values():
            if id == str(obj.id):
                return obj
        return None

    def count(self, cls=None):
        """ counts the number of instances of a class
        Args:
            cls: class name
        Return: count of instances of a class
        """
        return len(self.all(cls))

    def reload(self):
        """Loads storage dictionary from file"""

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            tmp = {}
            with open(FileStorage.__file_path, 'r') as f:
                tmp = json.load(f)
                for key, val in tmp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes and object from __objects"""
        if (obj):
            key = f"{type(obj).__name__}.{obj.id}"
            del self.__objects[key]

    def close(self):
        """Calls reload method for deserializing
        the JSON file to objects
        """
        self.reload()
