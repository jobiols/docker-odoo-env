# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.messages import Msg

msg = Msg()


class ConfigCommand(object):
    def __init__(self, data):
        self._data = data

    def execute(self):
        msg.run('Saved options')
        for item in self._data:
            msg.inf('{:11} -> {}'.format(item, str(self._data.get(item))))
