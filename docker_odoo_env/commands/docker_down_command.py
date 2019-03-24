# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.commands.command import Command
from docker_odoo_env.call import call
from docker_odoo_env.config import conf_


class DockerDownCommand(Command):
    def execute(self):
        if conf_.args.get('doc'):
            self.show_doc()

        # bajar todas las imagenes docker que esten activas
        command = 'sudo docker rm -f $(sudo docker ps -a -q)'
        call(command)
