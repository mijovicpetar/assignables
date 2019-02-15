"""Assignables module."""

from abc import ABC, abstractmethod
import copy
import inflection


class ValidationError(Exception):
    """Validation error exception."""
    def __init__(self, message):
        Exception.__init__(message)


class DataValidator(ABC):
    """Abstract validator."""

    @abstractmethod
    def validate(self, obj):
        """Abstract validate object."""


def apply_naming_convetion(val, naming_convention):
    """Apply naming convention.

    Args:
        val: Value to be changed.
        naming_convention: Convention to be used.
    Returns:
        Edited value or raises ValueError if naming convetion unknown.

    """
    if naming_convention == 'snake_case':
        res = inflection.underscore(val)
    elif naming_convention == 'camel_case':
        res = inflection.camelize(val, False)
    elif naming_convention == 'uper_camel_case':
        res = inflection.camelize(val)
    else:
        raise ValueError('Unknwon naming convetion.')

    return res


class Assignable:
    """Util class for property manipulation."""

    def __init__(self, unassignables=None, unserializables=None, validator=None):
        """Init Assignable object.

        Args:
            unassignables: Array of atributes to be ignored on assigning.
            unserializables: Array of atributes to be ignored on serializing.
        """
        # Setting unassignables.
        if unassignables is None:
            self._unassignables = ['id']
        else:
            self._unassignables = unassignables

        # Setting unserializables.
        if unserializables is None:
            self._unserializables = ['_sa_instance_state', '_unassignables',
                                      '_unserializables', '_validator']
        else:
            self._unserializables = unserializables

        # Setting validator.
        self._validator = validator


    def assign(self, data_dict, underscore_data=True):
        """Assign values from another object to current.

        Args:
            data: Data object.
            underscore_data: Flag for snake casing keys before assignment.
        Returns:
            Self object for Fluent design pattern.
            Raises ValidationError exception.

        """
        if self._validator is not None:
            validated = self._validator.validate(data_dict)
            if not validated:
                raise ValidationError('Validation failed.')

        obj_dict = self.__dict__
        for key in data_dict.keys():
            if underscore_data:
                # Python naming convetion is snake case.
                obj_key = inflection.underscore(key)
            else:
                obj_key = key

            if obj_key in self._unassignables:
                continue
            if obj_key not in obj_dict:
                continue
            if obj_dict[obj_key] != data_dict[key]:
                setattr(self, obj_key, data_dict[key])

        return self

    def get_json_dict(self, naming_convention=None):
        """Get json dict prepared for sending as response.

        Args:
            naming_convention: Naming convention to be applied.
        Returns:
            Dictionary representation.

        """
        json_dict = vars(self)
        # Creating copy to preserve original dict.
        json_dict = copy.deepcopy(json_dict)

        # Creating result dict.
        res_json_dict = {}
        for key in json_dict.keys():
            if key in self._unserializables:
                continue
            if naming_convention is None:
                uc_key = key
            else:
                uc_key = apply_naming_convetion(key, naming_convention)
            res_json_dict[uc_key] = json_dict[key]

        # Returning clean json dict.
        return res_json_dict
