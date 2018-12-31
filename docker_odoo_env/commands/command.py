# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.messages import Msg

msg = Msg()


class Command(object):
    def __init__(self, config):
        self._config = config

    def execute(self):
        raise NotImplementedError

    def show_doc(self):
        msg.text(self._config.args.get('command'))
        exit()
