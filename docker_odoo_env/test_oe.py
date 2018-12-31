# -*- coding: utf-8 -*-

import unittest
from docker_odoo_env.config import Config
from docker_odoo_env.commands.config_command import ConfigCommand
from docker_odoo_env.commands.update_command import UpdateCommand
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

    def test_02(self):
        """ Test config command
        """
        config = Config()
        config_command = ConfigCommand(config)
        config_command.execute()

    def test_03(self):
        config = Config()
        update_command = UpdateCommand(config)
        update_command.execute()