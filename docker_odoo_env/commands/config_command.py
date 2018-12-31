# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.commands.command import Command
from docker_odoo_env.messages import Msg

msg = Msg()


class ConfigCommand(Command):

    def execute(self):
        if self._config.args.get('doc'):
            self.show_doc()
        else:
            self._config.list()
