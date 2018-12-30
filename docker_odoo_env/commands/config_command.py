# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root


class ConfigCommand(object):
    def __init__(self, config):
        self._config = config

    def execute(self):
        self._config.list()
