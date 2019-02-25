# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root
import yaml
import os
from docker_odoo_env.messages import Msg

msg = Msg()

USER_CONFIG_PATH = os.path.expanduser('~') + '/.config/oe/'
USER_CONFIG_FILE = USER_CONFIG_PATH + 'config.yaml'
BASE_DIR = '/odoo_testing/'


class Config(object):
    def __init__(self):
        self._args = {}
        self._base_dir = BASE_DIR

    @staticmethod
    def clean_command_line(args):
        """ Elimina todos los parametros que no se requieren, convierte a dict
        """
        args = vars(args)
        for item in ['help']:
            if item in args:
                args.pop(item)
        return args

    @property
    def command(self):
        return self._args.get('command', False)

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        """ Le llegan los nuevos parametros de la linea de comandos, estos se
            mezclan con los que hay en configuracion teniendo precedencia los
            de la linea de comandos.
            Hace todos los valores persistentes y ajusta algunos valores por
            defecto.
            En self._args estan los parametros que usara el programa
        """
        # obtener la linea de comandos convertida a dict, eliminando algunos
        self._args = self.clean_command_line(value)

        # obtener el archivo de configuracion
        config = self.get_config()

        # Cliente actual, de los parametros, este siempre tiene precedencia
        client = self._args.get('client')

        # Fallback lo saco de la configuracion, y si tampoco esta es un error
        if not client:
            client = config.get('client')
            self._args['client'] = client

        # si aca no tengo definido el cliente termino con error
        if not client:
            msg.err('Need -c option (client name). Process aborted')

        # obtener la configuracion para el cliente actual.
        client_config = config.get(client, {})

        # Mezclo argumentos de linea de comandos con configuracion
        # la linea de comandos tiene precedencia
        for item in client_config or []:
            if item not in self._args:
                self._args[item] = client_config.get(item)

        # agregar valores por defecto si no estan definidos
        if not self._args.get('database'):
            self._args['database'] = self._args['client'] + '_prod'
        if not self._args.get('test_database'):
            self._args['test_database'] = self._args['client'] + '_test'

        self.save_config()

    def save_config(self):
        """ Salvar la configuracion que esta en self._args para el cliente
            para el cliente correspondiente.
        """
        if not os.path.exists(USER_CONFIG_PATH):
            os.makedirs(USER_CONFIG_PATH)

        # obtener el config actual
        config = self.get_config()

        # obtener el cliente
        client = self._args.get('client')

        # ciertos parametros no se tienen que salvar
        args = self._args.copy()
        for item in ['doc', 'command', 'client']:
            if item in args:
                args.pop(item)

        # actualizar el cliente default
        config['client'] = client

        # actualizar el resto de los parametros para ese cliente
        for item in args:
            if client in config:
                config[client][item] = args.get(item)
            else:
                config[client] = {item: args.get(item)}

        with open(USER_CONFIG_FILE, 'w') as config_file:
            yaml.dump(config, config_file, default_flow_style=False,
                      allow_unicode=True)

    @staticmethod
    def get_config():
        """
        :ret: Diccionario con la configuracion que hay en el yaml
        """
        try:
            with open(USER_CONFIG_FILE, 'r') as config:
                ret = yaml.safe_load(config)
        except Exception:
            return {}
        return ret if ret else {}

    def list(self):
        """ Listar las opciones del cliente por defecto y los demas clientes
        """

        config = self.get_config()
        client = config['client']
        default_config = config[client]

        msg.run('Saved options for client %s' % client)
        msg.inf('Default application (%s)' % default_config['defapp'])
        msg.inf('environment (%s)' % default_config['environment'])
        msg.inf('databases prod (%s) test (%s)' %
                (default_config['database'],
                 default_config['test_database']))
        msg.inf('Image (%s)' % default_config['image'])
        msg.inf('Nginx (%s) Debug (%s) Verbose (%s)' %
                (default_config['nginx'],
                 default_config['debug'],
                 default_config['verbose'])
                )
        msg.run('\nOther clients in this environment')
        clients = [item for item in config if item != 'client']

        msg.inf(', '.join(clients))

    def clear(self):
        self._args = {'client': 'none'}
        self.save_config()
