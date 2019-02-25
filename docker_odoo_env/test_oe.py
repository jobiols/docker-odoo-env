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
        # crea el objeto config
        config = Config()
        # borra todos los datos del config
        config.clear()

        # equivale a ponerle parametros  -c scaffolding
        config.args = argparse.Namespace(client='scaffolding',
                                         environment='prod',
                                         nginx='on',
                                         verbose='off',
                                         debug='off',
                                         defapp='http://github.com')
        data = config.args

        self.assertEqual(data.get('client'), 'scaffolding')
        self.assertEqual(data.get('database'), 'scaffolding_prod')
        self.assertEqual(data.get('test_database'), 'scaffolding_test')
        self.assertEqual(data.get('environment'), 'prod')
        self.assertEqual(data.get('nginx'), 'on')
        self.assertEqual(data.get('verbose'), 'off')
        self.assertEqual(data.get('debug'), 'off')

        config = Config()
        config.args = argparse.Namespace(client='client_test_01',
                                         environment='staging',
                                         nginx='off',
                                         verbose='on',
                                         debug='on',
                                         defapp='http://github.com')
        data = config.args
        self.assertEqual(data.get('client'), 'client_test_01')
        self.assertEqual(data.get('database'), 'client_test_01_prod')
        self.assertEqual(data.get('test_database'), 'client_test_01_test')
        self.assertEqual(data.get('environment'), 'staging')
        self.assertEqual(data.get('nginx'), 'off')
        self.assertEqual(data.get('verbose'), 'on')
        self.assertEqual(data.get('debug'), 'on')

    def test_02(self):
        """ Test config command
        """
        config = Config()
        config_command = ConfigCommand(config)
        config_command.execute()

    def test_03(self):
        config = Config()
        config.args['client'] = 'scaffolding'
        config.args['defapp'] = 'https://github.com/jobiols/cl-scaffolding.git'
        update_command = UpdateCommand(config)
        update_command.execute()

    def test_04(self):
        """ Create hierarchy
        """
        config = Config()
        config._base_dir = os.path.expanduser('~/') + 'odoo_test/'

        import shutil
        if os.path.isdir(config._base_dir):
            shutil.rmtree(config._base_dir)

        config.args['client'] = 'scaffolding'
        config.args['defapp'] = 'https://github.com/jobiols/cl-scaffolding.git'
        hierarchy = DirectoryHierarchyCommand(config)
        hierarchy.execute()

    def test_05(self):
        """ Chequear manifest
        """
        manifest_path = os.path.expanduser(
            '~/') + 'odoo_test/.scaffolding_default/scaffolding_default'

        manifest = OdooManifest(manifest_path, 'scaffolding')
        repos = [
            {'usr': 'jobiols', 'repo': 'cl-vhing', 'branch': '11.0'},
            {'usr': 'jobiols', 'repo': 'odoo-addons', 'branch': '11.0'},
            {'usr': 'jobiols', 'repo': 'rafi16jan-backend-theme',
             'branch': '11.0'},

            {'usr': 'jobiols', 'repo': 'adhoc-odoo-argentina',
             'branch': '11.0'},
            {'usr': 'jobiols', 'repo': 'adhoc-argentina-sale',
             'branch': '11.0'},
            {'usr': 'jobiols', 'repo': 'adhoc-account-financial-tools',
             'branch': '11.0'},
            {'usr': 'jobiols', 'repo': 'adhoc-account-payment',
             'branch': '11.0'},
            {'usr': 'jobiols', 'repo': 'adhoc-miscellaneous',
             'branch': '11.0'},
            {'usr': 'jobiols', 'repo': 'adhoc-argentina-reporting',
             'branch': '11.0'},
            {'usr': 'jobiols', 'repo': 'adhoc-reporting-engine',
             'branch': '11.0'},
            {'usr': 'jobiols', 'repo': 'adhoc-aeroo_reports',
             'branch': '11.0'},
            {'usr': 'jobiols', 'repo': 'oca-partner-contact',
             'branch': '11.0'},
            {'usr': 'jobiols', 'repo': 'oca-web', 'branch': '11.0'},
            {'usr': 'jobiols', 'repo': 'oca-server-tools', 'branch': '11.0'}, ]
        self.assertEqual(repos, manifest.repos)

        docker = [
            {'name': 'odoo', 'usr': 'jobiols', 'img': 'odoo-jeo',
             'ver': '11.0'},
            {'name': 'postgres', 'usr': 'postgres', 'ver': '11.1-alpine'},
            {'name': 'nginx', 'usr': 'nginx', 'ver': 'latest'},
            {'name': 'aeroo', 'usr': 'adhoc', 'img': 'aeroo-docs'}, ]
        self.assertEqual(docker, manifest.docker)
        self.assertEqual('11.0', manifest.version)
        self.assertEqual(11.0, manifest.numeric_version)
