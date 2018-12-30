# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.messages import Msg

msg = Msg()


class ConfigCommand(object):
    def __init__(self, config):
        self._config = config

    def execute(self):
        msg.run('Saved options')
        self._config.list()
