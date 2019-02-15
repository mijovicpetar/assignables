# Assignables #
## Helper package for Flask and Flask-API ##

## Third Party Library Requirements ##
* inflection

## Introduction ##

This package is helper package for assigning values to SqlAlchemy db model objects and to get their dict representation so they can be sent as response for Flask-API endpoints.

## Installation ##
    pip install assignables

## Usage ##
    from assignables import Assignable

    def class SomeModel(db.Model, Assignable):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

        def __init__(self, username, email):
            Assignable.__init__()
            self.username = username
            self.email = email

Assignable will give your model two new methods:
1. `assign(data_dict)` - this method will assign coresponding atributes from respective key valu pairs from `data_dict`.
2. `get_json_dict()` - this method will return objects dictionary.

Using `assign` method will by default not assign objects `id`, but will other atributes if they exist in `data_dict`.
Method `get_json_dict` will not have `_sa_instance_state` key inside by default and atriubets Assignable contains.

If you want to specify custom atributes for not assigning or not serializing you can do that:
    from assignables import Assignables

    class SomeModel(db.Model, Assignable):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

        def __init__(self, username, email):
            Assignable.__init__(unassignables=unassignables, unserializables=unserializables)
            unassignables = ['id', 'email']
            unserializables = ['_sa_instance_state', 'email']
            self.username = username
            self.email = email

If used like this, `assign` method will not assign `id` and `email` atributes.
Dictinary returned by calling `get_json_dict` will not have keys `_sa_instance_state` and `email`.
