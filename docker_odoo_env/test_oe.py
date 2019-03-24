# -*- coding: utf-8 -*-

import unittest
from docker_odoo_env.commands.config_command import ConfigCommand
from docker_odoo_env.commands.pull_command import PullCommand
from docker_odoo_env.commands.odoo_conf_command import OdooConfCommand
from docker_odoo_env.config import conf_
from docker_odoo_env.commands.directory_hierarchy_command import \
    DirectoryHierarchyCommand
from docker_odoo_env.config import OdooManifest
import argparse


class TestRepository(unittest.TestCase):
    def setUp(self):
        # cambiar el base dir para que no rompa las cosas en mi maquina.
        conf_.base_dir = '/odoo_test/'

    def test_01(self):
        """ Save and restore config
        """
        # equivale a ponerle parametros  -c scaffolding
        conf_.args = argparse.Namespace(client='scaffolding',
                                        environment='prod',
                                        nginx='on',
                                        verbose='off',
                                        debug='off',
                                        defapp='https://github.com/jobiols/cl-scaffolding.git')
        data = conf_.args

        self.assertEqual(data.get('client'), 'scaffolding')
        self.assertEqual(data.get('database'), 'scaffolding_prod')
        self.assertEqual(data.get('test_database'), 'scaffolding_test')
        self.assertEqual(data.get('environment'), 'prod')
        self.assertEqual(data.get('nginx'), 'on')
        self.assertEqual(data.get('verbose'), 'off')
        self.assertEqual(data.get('debug'), 'off')

        conf_.args = argparse.Namespace(client='client_test_01',
                                        environment='staging',
                                        nginx='off',
                                        verbose='on',
                                        debug='on',
                                        defapp='http://github.com')
        data = conf_.args
        self.assertEqual(data.get('client'), 'client_test_01')
        self.assertEqual(data.get('database'), 'client_test_01_prod')
        self.assertEqual(data.get('test_database'), 'client_test_01_test')
        self.assertEqual(data.get('environment'), 'staging')
        self.assertEqual(data.get('nginx'), 'off')
        self.assertEqual(data.get('verbose'), 'on')
        self.assertEqual(data.get('debug'), 'on')

    def test_02(self):
        """ Chequear manifest
        """
        conf_.args = argparse.Namespace(client='scaffolding',
                                        environment='prod',
                                        nginx='on',
                                        verbose='off',
                                        debug='off',
                                        defapp='https://github.com/jobiols/cl-scaffolding.git')
        manifest = OdooManifest(conf_)
        repos = [
            'https://github.com/jobiols/cl-scaffolding.git',
            'https://github.com/jobiols/odoo-addons.git',
            'https://github.com/jobiols/adhoc-odoo-argentina.git'
        ]
        self.assertEqual(repos, manifest.git_repos)

        docker = [
            {'img': 'jobiols/odoo-jeo:11.0', 'name': 'odoo'},
            {'img': 'postgres:11.1-alpine', 'name': 'postgres'},
            {'img': 'adhoc/aeroo', 'name': 'aeroo'}
        ]
        _ = manifest.docker_images
        self.assertEqual(docker, _)
        self.assertEqual('11.0', manifest.version)
        self.assertEqual(11.0, manifest.numeric_version)

    def test_03(self):
        """ Test config command
        """
        # ejecutar el comando config, tiene que mostrar la configuracion del
        # cliente client_test_01
        config_command = ConfigCommand()
        config_command.execute()

    def test_04(self):
        """ Create hierarchy
        """
        # borrar la estructura de directorios en disco
        import shutil
        shutil.rmtree(conf_.base_dir, ignore_errors=True)

        conf_.args['client'] = 'scaffolding'
        conf_.args['defapp'] = 'https://github.com/jobiols/cl-scaffolding.git'
        hierarchy = DirectoryHierarchyCommand()
        hierarchy.execute()

    def test_05(self):
        """Testear backup
        """

        # borrar la estructura de directorios en disco
        import shutil
        shutil.rmtree(conf_.base_dir, ignore_errors=True)

        # configurar el cliente scaffolding
        conf_.args['client'] = 'scaffolding'
        conf_.args['defapp'] = 'https://github.com/jobiols/cl-scaffolding.git'

        # ejecutar comando backup
        from docker_odoo_env.commands.update_command import BackupCommand
        backup_command = BackupCommand()
        backup_command.execute()

def test_06(self):
    """ Testear bajada de imagenes de memoria
    """
    # configurar el cliente scaffolding
    conf_.args['client'] = 'scaffolding'
    conf_.args['defapp'] = 'https://github.com/jobiols/cl-scaffolding.git'

    # Baja todas las imagenes docker (si estan activas)
    from docker_odoo_env.commands.docker_down_command import DockerDownCommand
    command = DockerDownCommand()
    command.execute()

def test_07(self):
    """  hace clone o pull de todos los repos y las imagenes
    """
    command = PullCommand()
    command.execute()

def test_08(self):
    """ crea, actualiza el odoo.conf, segun en que ambiente estemos
    """
    command = OdooConfCommand()
    command.execute()
