# -*- coding: utf-8 -*-

import unittest
from parse_args import save_config, get_config


class TestRepository(unittest.TestCase):
    def test_01(self):
        """ Save and restore config
        """
        data = {
            'item1': 1,
            'item2': 2,
            'item3': ['first', 'second', 'off']
        }

        save_config(data)
        self.assertEqual(data, get_config())
