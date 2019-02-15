"""Assignables tests."""

import sys
import os
import unittest

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DIR_PATH = os.path.abspath(os.path.join(DIR_PATH, os.pardir))
sys.path.append(DIR_PATH)

import assignables


class TestClass(assignables.Assignable):
    """Test model class."""
    def __init__(self, arg1=None, arg2=None, arg3=None):
        """Init model object."""
        assignables.Assignable.__init__(self)
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3


class AssignableTest(unittest.TestCase):
    """Assignables unit tests."""

    def test_assigning(self):
        """Test assign method."""
        data_dict = {
            "arg1": 1,
            "arg2": "2",
            "arg3": None
        }

        obj = TestClass()
        obj.assign(data_dict)

        if obj.arg1 != data_dict['arg1']:
            self.fail('Obj arg1 not assigned: ' + str(obj.arg1))
        if obj.arg2 != data_dict['arg2']:
            self.fail('Obj arg2 not assigned: ' + str(obj.arg2))
        if obj.arg3 != data_dict['arg3']:
            self.fail('Obj arg3 not assigned: ' + str(obj.arg3))

    def test_serialization(self):
        """Test serialization."""
        data_dict = {
            "arg1": 1,
            "arg2": "2",
            "arg3": None
        }

        obj = TestClass()
        obj.assign(data_dict)
        res_dict = obj.get_json_dict()

        for key in res_dict.keys():
            if data_dict[key] != res_dict[key]:
                self.fail(key + ' not serialized correctly.')

if __name__ == '__main__':
    unittest.main()
