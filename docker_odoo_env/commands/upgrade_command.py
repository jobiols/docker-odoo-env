# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.commands.command import Command


class UpgradeCommand(Command):

    def execute(self):
        if self._config.args.get('doc'):
            self.show_doc()
