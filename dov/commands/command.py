# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.messages import msg
from docker_odoo_env.config import conf_
import os, pwd
from docker_odoo_env.call import call


class Command(object):
    def execute(self):
        raise NotImplementedError

    @staticmethod
    def show_doc():
        msg.text(conf_.args.get('command'))
        exit()

    @staticmethod
    def repo_exist(repo):
        repo_dir = conf_.client_dir + repo[repo.rfind('/'):repo.rfind('.git')]
        return os.path.exists(repo_dir)

    @staticmethod
    def create_struct():
        msg.inf('Creating directory structure')
        if not os.path.isdir(conf_.base_dir):
            command = 'sudo mkdir {}'.format(conf_.base_dir)
            call(command)

        # cambiar ownership por el de usuario que esta usando esto.
        username = pwd.getpwuid(os.getuid()).pw_name
        command = 'sudo chown {0}:{0} {1}'.format(username, conf_.base_dir)
        call(command)

        client_dir = '{}odoo-{}/{}/'.format(conf_.base_dir,
                                            conf_.manifest.version,
                                            conf_.args['client'])

        # crear la jerarquia de directorios
        for w_dir in ['postgresql', 'config', 'data_dir', 'backup_dir',
                      'log', 'sources']:
            os.makedirs(client_dir + w_dir, 0o777)
