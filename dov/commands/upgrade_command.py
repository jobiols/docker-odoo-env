# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.commands.command import Command
from docker_odoo_env.config import conf_
from docker_odoo_env.messages import msg
from docker_odoo_env.call import call
import os


class UpgradeCommand(Command):
    def execute(self):
        if conf_.args.get('doc'):
            self.show_doc()

        # Actualizar el sistema operativo
        msg.inf('Updating Server')
        command = 'sudo apt-get update && sudo apt-get upgrade -y'
        call(command)

        # Baja las imagenes de docker
        for img in conf_.manifest.docker_images:
            command = 'sudo docker pull ' + img['img']
            call(command)
