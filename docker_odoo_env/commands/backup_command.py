# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.commands.command import Command


class BackupCommand(Command):

    def execute(self):
        if self._config.args.get('doc'):
            self.show_doc()

        # verificar si esta arriba la imagen de docker, si no lo esta no se
        # puede hacer backcup