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
