# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root
import yaml
import os
from docker_odoo_env.messages import Msg

msg = Msg()

user_config_path = os.path.expanduser('~') + '/.config/oe/'
user_config_file = user_config_path + 'config.yaml'


class Config(object):
    def __init__(self):
        self._args = {}

    @property
    def command(self):
        return self._args.get('command', False)

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        """ le llegan los nuevos parametros del argsparse y los hace
            persistentes
        """
        # convertir value, que son los args del argsparse a dict
        self._args = vars(value)

        # obtener el config actual de disco
        config = self.get_config()

        # pasar las cosas que estan en config y no estan definidas en args
        for item in config or []:
            if not self._args.get(item) and config.get(item):
                self._args[item] = config.get(item, None)

        # agregar el default para databases
        if not self._args.get('database') and self._args.get('client'):
            self._args['database'] = self._args['client'] + '_prod'
            self._args['test_database'] = self._args['client'] + '_test'

        self.save_config()

    def save_config(self):
        if not os.path.exists(user_config_path):
            os.makedirs(user_config_path)
        with open(user_config_file, 'w') as config:
            yaml.dump(self._args, config, default_flow_style=False,
                      allow_unicode=True)

    @staticmethod
    def get_config():
        """
        :ret: Diccionario con la configuracion que hay en el yaml
        """
        try:
            with open(user_config_file, 'r') as config:
                ret = yaml.safe_load(config)
        except Exception:
            return False
        return ret

    def list(self):
        msg.run('Saved options')
        for item in self._args:
            msg.inf('{:11} -> {}'.format(item, str(self._args.get(item))))

    def clear(self):
        self._args = dict
        self.save_config()
