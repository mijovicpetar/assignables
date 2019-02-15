# Assignables #
Helper package for Flask and Flask-API

## Third Party Library Requirements ##
* inflection

## Introduction ##

This package is helper package for assigning values to SqlAlchemy db model objects and to get their dict representation so they can be sent as response for Flask-API endpoints. This package can be used without using SqlAlchemy, Flask and Flask-API.

## Installation ##
    pip install assignables

## Usage ##
    from assignables import Assignable

    class SomeModel(db.Model, Assignable):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

        def __init__(self, username=None, email=None):
            Assignable.__init__()
            self.username = username
            self.email = email

    data = {
        "username": 'user123',
        "email": 'user@email.com'
    }

    obj = SomeModel()
    obj.assign(data) # username and email will be assigned.

    obj_dict = obj.get_json_dict() # obj_dict won't contain _sa_instance_state and Assignable class atributes.

Assignable will give your model two new methods:
1. `assign(data_dict)` - this method will assign coresponding atributes from respective key value pairs from `data_dict`.
2. `get_json_dict()` - this method will return objects dictionary.

Using `assign` method will by default not assign objects `id`, but will other atributes if they exist in `data_dict`.
Method `get_json_dict` will not have `_sa_instance_state` key inside by default and atriubets Assignable contains.

If you want to specify custom atributes for not assigning or not serializing you can do that:
    from assignables import Assignables

    class SomeModel(db.Model, Assignable):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

        def __init__(self, username=None, email=None):
            unassignables = ['id', 'email']
            unserializables = ['_sa_instance_state', 'email']
            Assignable.__init__(unassignables=unassignables, unserializables=unserializables)
            self.username = username
            self.email = email

    data = {
        "username": 'user123',
        "email": 'user@email.com'
    }

    obj = SomeModel()
    obj.assign(data) # username will only be assigned.

    obj_dict = obj.get_json_dict() # obj_dict will not contain _sa_instance_state and email atributes.

If used like this, `assign` method will not assign `id` and `email` atributes.
Dictinary returned by calling `get_json_dict` will not have keys `_sa_instance_state` and `email`.

You can also add you custom data validator - Validation will be executed inside `assign` method.
If validation failed `ValidationError` exception is raised.

    from assignables import DataValidator, Assignables


    class CustomValidator(DataValidator):
        def validate(self, obj):
            # return True if validated, false otherwise.


    class SomeModel(db.Model, Assignable):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

        def __init__(self, username=None, email=None):
            Assignable.__init__(validator=CustomValidator())
            self.username = username
            self.email = email

    data = {
            "username": 'user123',
            "email": 'user@email.com'
        }

    obj = SomeModel()
    obj.assign(data) # Data will be validate using you custom data validator.

If there is a missmatch between you atribute naming or you wish to specify a naming convetion for
resulting dictionary there is a way.

    data = {
            "Username": 'user123',
            "Email": 'user@email.com'
        }

    obj = SomeModel()
    obj.assign(data, under_score_data=True) # This will handle create snake case keys from data dictionary keys.
    obj_dict = obj.get_json_dict(naming_convetion='camel_case') # Output dict would have camel case keys.

Options for `naming_convention` are:
1. camel_case
2. upper_camel_case
3. snake_case
