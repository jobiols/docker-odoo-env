# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.commands.command import Command

import os
from docker_odoo_env.call import call
import pwd
import yaml
from docker_odoo_env.messages import Msg

msg = Msg()

IN_CONFIG = '/opt/odoo/etc/'
IN_DATA = '/opt/odoo/data'
IN_LOG = '/var/log/odoo'
IN_CUSTOM_ADDONS = '/opt/odoo/custom-addons'
IN_EXTRA_ADDONS = '/opt/odoo/extra-addons'
IN_DIST_PACKAGES = '/usr/lib/python{}/dist-packages'
IN_DIST_LOCAL_PACKAGES = '/usr/local/lib/python{}/dist-packages'
IN_BACKUP_DIR = '/var/odoo/backups/'


class OdooManifest(object):
    def __init__(self, manifest_path, client):
        self._manifest = self.get_manifest(manifest_path, client)

    @property
    def repos(self):
        return self._manifest['repos']

    @property
    def docker(self):
        return self._manifest['docker']

    @property
    def version(self):
        ver = self._manifest['version']
        # encontrar primer punto
        pos = ver.find('.') + 1
        # encontrar segundo punto
        pos = ver[pos:].find('.') + pos
        # devolver "mayor.minor"
        return ver[:pos]

    @property
    def numeric_version(self):
        return float(self.version)

    def get_manifest(self, path, client):
        """
        :param path: base dir to walk searching for manifest
        :return: parsed manifest file as dictionary
        """
        for root, dirs, files in os.walk(path):
            for file in ['__openerp__.py', '__manifest__.py']:
                if file in files:
                    manifest_file = '{}/{}'.format(root, file)
                    manifest = self.load_manifest(manifest_file)
                    # get first word of name in lowercase
                    name = manifest.get('name').lower()
                    name = name.split()[0]
                    if name == client:
                        return manifest

    @staticmethod
    def load_manifest(filename):
        """
        Loads a manifest
        :param filename: absolute filename to manifest
        :return: manifest in dictionary format
        """
        manifest = ''
        with open(filename, 'r') as f:
            for line in f:
                if line.strip() and line.strip()[0] != '#':
                    manifest += line
            try:
                ret = eval(manifest)
            except Exception:
                return {'name': 'none'}
            return ret


class DirectoryHierarchyCommand(Command):
    def execute(self):
        if self._config.args.get('doc'):
            self.show_doc()

        # chequear si existe
        if not os.path.isdir(self._config._base_dir):
            self.create_struct()

    def create_struct(self):
        msg.inf('Creating directory structure')

        # crear base dir con sudo
        command = 'sudo mkdir {}'.format(self._config._base_dir)
        call(command)

        # cambiar ownership
        username = pwd.getpwuid(os.getuid()).pw_name
        command = 'sudo chown {0}:{0} {1}'.format(username, self._config._base_dir)
        call(command)

        # preparar la bajada de la aplicacion default
        client = '.default_' + self._config.args['client']
        defapp = self._config.args['defapp']
        aggregator_config = {
            client: {
                'remotes': {
                    'default': defapp
                },
                'merges': ['default 9.0'],
                'target': 'default 9.0'
            }
        }
        # bajar la default app temporariamente solo para leer el manifest
        with open(self._config._base_dir + 'defapp.yaml', 'w') as config:
            yaml.dump(aggregator_config, config, default_flow_style=False,
                      allow_unicode=True)

        # aggregator baja el repo en en current dir
        os.chdir(self._config._base_dir)
        command = 'gitaggregate -c ' + self._config._base_dir + 'defapp.yaml'
        call(command)

        # leer el manifest
        manifest_path = self._config._base_dir + '.default_iomaq/iomaq_default/'
        manifest = OdooManifest(manifest_path, self._config.args['client'])

        base_dir = '{}odoo-{}/'.format(self._config._base_dir, manifest.version,
                                       self._config.args['client'])

        # crear el resto de la jerarquia
        for w_dir in ['postgresql', 'config', 'data_dir', 'backup_dir', 'log',
                      'sources']:

            r_dir = '{}{}'.format(base_dir, w_dir)
            command = 'mkdir -p {}'.format(r_dir),
            call(command)
