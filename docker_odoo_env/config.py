# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root
import yaml
import os
from docker_odoo_env.messages import msg
from docker_odoo_env.call import call
import tempfile
import shutil

USER_CONFIG_PATH = os.path.expanduser('~') + '/.config/oe/'
USER_CONFIG_FILE = USER_CONFIG_PATH + 'config.yaml'
BASE_DIR = '/odoo_testing/'
EPHEMERAL_PARAMETERS = ['doc', 'command', 'client', 'database_file']


class OdooManifest(object):
    def __init__(self, config):
        self._config = config
        self._client = config._args['client']
        self._manifest = self.get_manifest()

    def get_manifest(self):
        """ Buscar la app manifest en la estructura de directorios
            Usar un cache para encontrarla mas rapido
            Si no la encuentro bajar la app defautl y leerle el manifest
        """

        # buscar el manifest en la estructura de directorios
        manifest = self.get_manifest_from_struct(path=self._config.base_dir)
        if manifest:
            return manifest

        tmpdir = tempfile.mkdtemp()
        try:
            # si no lo encuentra bajar la app default y leerlo de ahi
            command = 'git -C {} clone --depth 1 {} tmp'.format(
                tmpdir,
                self._config.args['defapp'])

            call(command)
            manifest = self.get_manifest_from_struct(path=tmpdir)
        finally:
            shutil.rmtree(tmpdir)

        if not manifest:
            msg.err('Client {} not found'.format(self._client))

        return manifest

    def get_manifest_from_struct(self, path):
        """ leer un manifest que esta dentro de una estructura de directorios
            revisar toda la estructura hasta encontrar un manifest.
        """
        for root, dirs, files in os.walk(path):
            for file in ['__openerp__.py', '__manifest__.py']:
                if file in files:
                    manifest_file = '{}/{}'.format(root, file)
                    manifest = self.load_manifest(manifest_file)

                    # get first word of name in lowercase
                    name = manifest.get('name').lower()
                    name = name.split()[0]
                    if name == self._client:
                        return manifest
        return False

    @property
    def git_repos(self):
        ret = self._manifest.get('git-repos')
        if not ret:
            msg.err('Manifest has no repositories')
        return ret

    @property
    def docker_images(self):
        ret = self._manifest.get('docker-images')
        if not ret:
            msg.err('Manifest has no images')
        return ret

    @property
    def version(self):
        ver = self._manifest['version']
        if not ver:
            msg.err('Manifest has no version')
        # encontrar primer punto
        pos = ver.find('.') + 1
        # encontrar segundo punto
        pos = ver[pos:].find('.') + pos
        # devolver "mayor.minor"
        return ver[:pos]

    @property
    def numeric_version(self):
        return float(self.version)

    @property
    def Enterprise(self):
        ver = self._manifest.get('enterprise')
        if not ver:
            msg.err('Manifest has no Enterprise')
        else:
            return ver

    @staticmethod
    def load_manifest(filename):
        """
        Loads a manifest
        :param filename: absolute filename to manifest
        :return: manifest in dictionary format
        """
        manifest = ''
        with open(filename, 'r') as f:
            for line in f:
                if line.strip() and line.strip()[0] != '#':
                    manifest += line
            try:
                ret = eval(manifest)
            except Exception:
                return {'name': 'none'}
            return ret


class Config(object):
    def __init__(self):
        self._args = {}
        self.base_dir = BASE_DIR
        self._app_cache = []
        self._manifest = False

    @property
    def client_dir(self):
        return '{}odoo-{}/{}'.format(self.base_dir,
                                     self.manifest.version,
                                     self.args['client'])

    @property
    def manifest(self):
        """ Si no tengo el manifest lo creo
        """
        if not self._manifest:
            self._manifest = OdooManifest(self)
        return self._manifest

    @staticmethod
    def clean_command_line(args):
        """ Elimina todos los parametros que no se requieren, convierte a dict
        """
        args = vars(args)
        # solo devuelvo los items que tienen datos en el runstring
        ret = {}
        for item in args:
            if args[item]:
                ret[item] = args[item]
        return ret

    def add_default_values(self):
        args = self._args
        if not args.get('database'):
            args['database'] = args['client'] + '_prod'

        if not args.get('test_database'):
            args['test_database'] = args['client'] + '_test'

        if not args.get('nginx'):
            args['nginx'] = 'on'

        if not args.get('debug'):
            args['debug'] = 'off'

        if not args.get('verbose'):
            args['verbose'] = 'off'

        if not args.get('environment'):
            args['environment'] = 'prod'

        if not args.get('image'):
            args['image'] = 'Manifest Image'

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
        self.add_default_values()

        # si aca no tengo definido la aplicacion default termino con error
        if not self._args.get('defapp'):
            msg.err('Need --defapp option (default application). '
                    'Process aborted')

        self.save_config()

    def save_config(self):
        """ Salvar la configuracion que esta en self._args para el cliente
            correspondiente.
        """
        if not os.path.exists(USER_CONFIG_PATH):
            os.makedirs(USER_CONFIG_PATH)

        # obtener el config actual
        config = self.get_config()

        # obtener el cliente
        client = self._args.get('client')

        # ciertos parametros no se tienen que salvar
        args = self._args.copy()
        for item in EPHEMERAL_PARAMETERS:
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

        # actualizar el cache de aplicaciones
        config['app_cache'] = self._app_cache

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

        msg.show(client, default_config)
        msg.run('\nOther clients in config')
        clients = [item for item in config if item != 'client']
        msg.inf(', '.join(clients))

    def clear(self):
        self._args = {'client': 'none'}
        self.save_config()


conf_ = Config()
