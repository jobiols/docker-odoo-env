# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.commands.command import Command
from docker_odoo_env.config import conf_
from docker_odoo_env.call import call


class PullCommand(Command):
    def execute(self):
        if conf_.args.get('doc'):
            self.show_doc()

        # Actualiza o crea los repositorios
        for rep in conf_.manifest.git_repos:
            if self.repo_exist(rep):
                command = 'git -C {} pull {}'.format(conf_.client_dir, rep)
            else:
                command = 'git -C {} clone {}'.format(conf_.client_dir, rep)
            call(command)
