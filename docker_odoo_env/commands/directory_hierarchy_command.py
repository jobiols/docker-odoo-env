# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.commands.command import Command
import os
from docker_odoo_env.call import call
import pwd
from docker_odoo_env.messages import msg
from docker_odoo_env.config import conf_

IN_CONFIG = '/opt/odoo/etc/'
IN_DATA = '/opt/odoo/data'
IN_LOG = '/var/log/odoo'
IN_CUSTOM_ADDONS = '/opt/odoo/custom-addons'
IN_EXTRA_ADDONS = '/opt/odoo/extra-addons'
IN_DIST_PACKAGES = '/usr/lib/python{}/dist-packages'
IN_DIST_LOCAL_PACKAGES = '/usr/local/lib/python{}/dist-packages'
IN_BACKUP_DIR = '/var/odoo/backups/'


class DirectoryHierarchyCommand(Command):
    def execute(self):
        if conf_.args.get('doc'):
            self.show_doc()

        # chequear si existe el path a cl-cliente
        if not os.path.isdir(conf_.client_dir):
            self.create_struct()

    def create_struct(self):
        msg.inf('Creating directory structure')

        # crear base dir con sudo
        command = 'sudo mkdir {}'.format(conf_.base_dir)
        call(command)

        # cambiar ownership por el de usuario que esta usando esto.
        username = pwd.getpwuid(os.getuid()).pw_name
        command = 'sudo chown {0}:{0} {1}'.format(username,
                                                  conf_.base_dir)
        call(command)
        client_dir = '{}odoo-{}/{}/'.format(conf_.base_dir,
                                            conf_.manifest.version,
                                            conf_.args['client'])

        # crear el resto de la jerarquia
        for w_dir in ['postgresql', 'config', 'data_dir', 'backup_dir',
                      'log', 'sources']:
            r_dir = '{}{}'.format(client_dir, w_dir)
            command = 'mkdir -p {}'.format(r_dir)
            call(command)
