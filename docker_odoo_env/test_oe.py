# -*- coding: utf-8 -*-

import unittest
from docker_odoo_env.config import Config
import argparse


class TestRepository(unittest.TestCase):
    def test_01(self):
        """ Save and restore config
        """
        config = Config()
        config.clear()

        config.args = argparse.Namespace(client='iomaq', dos=2)
        data = config.args

        self.assertEqual(data.get('client'), 'iomaq')
        self.assertEqual(data.get('database'), 'iomaq_prod')
        self.assertEqual(data.get('test_database'), 'iomaq_test')
