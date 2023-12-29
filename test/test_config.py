#!/bin/
import unittest

from etoro_bot import config

class TestStringMethods(unittest.TestCase):

    def test_config(self):
        assert config.etoro_user != None, "Not loaded config values"
        assert config.etoro_pwd != None, "Not loaded config values"

if __name__ == '__main__':
    unittest.main()