# -*- coding: utf-8 -*-

import unittest
from docker_odoo_env.config import Config
from docker_odoo_env.commands.config_command import ConfigCommand
from docker_odoo_env.commands.update_command import UpdateCommand
from docker_odoo_env.commands.directory_hierarchy_command import \
    DirectoryHierarchyCommand
from docker_odoo_env.commands.directory_hierarchy_command import OdooManifest
import argparse
import os


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
        config.args['client'] = 'iomaq'
        config.args['defapp'] = 'https://github.com/jobiols/cl-iomaq.git'
        update_command = UpdateCommand(config)
        update_command.execute()

    def test_04(self):
        """ Create hierarchy
        """
        config = Config()
        config._base_dir = '~/odoo_test/'

        import shutil
        if os.path.isdir(config._base_dir):
            shutil.rmtree(config._base_dir)

        config.args['client'] = 'iomaq'
        config.args['defapp'] = 'https://github.com/jobiols/cl-iomaq.git'
        hierarchy = DirectoryHierarchyCommand(config)
        hierarchy.execute()

    def test_05(self):
        """ Chequear manifest
        """
        manifest_path = os.path.abspath(__file__).strip('test_oe.py') + 'doc/'
        manifest = OdooManifest(manifest_path, 'iomaq')
        repos = [
            {'usr': 'jobiols', 'repo': 'cl-iomaq', 'branch': '9.0'},
            {'usr': 'jobiols', 'repo': 'odoo-addons', 'branch': '9.0'},
            {'usr': 'Vauxoo', 'repo': 'addons-vauxoo', 'branch': '9.0'},
        ]
        self.assertEqual(repos, manifest.repos)

        docker = [
            {'name': 'aeroo', 'usr': 'jobiols', 'img': 'aeroo-docs'},
            {'name': 'odoo', 'usr': 'jobiols', 'img': 'odoo-jeo',
             'ver': '9.0'},
            {'name': 'postgres', 'usr': 'postgres', 'ver': '9.5'},
            {'name': 'nginx', 'usr': 'nginx', 'ver': 'latest'}
        ]
        self.assertEqual(docker, manifest.docker)
        self.assertEqual('9.0', manifest.version)
        self.assertEqual(9.0, manifest.numeric_version)
