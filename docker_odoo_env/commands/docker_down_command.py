# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.commands.command import Command


class DockerDownCommand(Command):
    def __init__(self, config):
        self._config = config

    def execute(self):
        pass
