# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root


class Command(object):
    def __init__(self, config):
        self._config = config

    def execute(self):
        raise NotImplementedError