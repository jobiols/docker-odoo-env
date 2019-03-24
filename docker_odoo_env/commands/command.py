# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.messages import msg
from docker_odoo_env.config import conf_


class Command(object):

    def execute(self):
        raise NotImplementedError

    @staticmethod
    def show_doc():
        msg.text(conf_.args.get('command'))
        exit()
