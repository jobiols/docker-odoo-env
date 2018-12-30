# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import yaml
import argparse
from docker_odoo_env.__init__ import __version__
from docker_odoo_env.messages import Msg

msg = Msg()

user_config_path = os.path.expanduser('~') + '/.config/oe/'
user_config_file = user_config_path + 'config.yaml'


def merge_args(args, config):
    """
    A los datos que estan en args les agrega los datos que vienen en config

    :param args: (namespace) argumentos del parser
    :param config: (dictionary) argumentos del config.yml
    :return: args + config (dictionary)
    """
    # convertir args a dict
    ret = vars(args)

    # pasar a ret las cosas que estan en config y no estan definidas en ret
    for item in config or []:
        if not ret.get(item) and config.get(item):
            ret[item] = config.get(item, None)

    # agregar el default para databases
    if not ret.get('database') and ret.get('client'):
        ret['database'] = ret['client'] + '_prod'
        ret['test_database'] = ret['client'] + '_test'

    return ret


def command_config(data):
    msg.run('Saved options')
    for item in data:
        msg.inf('{:11} -> {}'.format(item, str(data.get(item))))


def command_update(data):
    """
        Las siguientes opciones son requeridas o deben estar almacenadas
        client
        Si falta alguna se aborta y se muestra el error

    :param data: Diccionario con las opciones a aplicar
    :return: None
    """
    if not data.get('client'):
        msg.err('Must define a client')


def save_config(data):
    if not os.path.exists(user_config_path):
        os.makedirs(user_config_path)
    with open(user_config_file, 'w') as config:
        yaml.dump(data, config, default_flow_style=False, allow_unicode=True)


def get_config():
    try:
        with open(user_config_file, 'r') as config:
            ret = yaml.safe_load(config)
    except Exception:
        return False
    return ret


def new_config_parser(sub):
    parser = sub.add_parser('config',
                            help='config current configuration')
    parser.add_argument('-c',
                        dest='client',
                        help='Client name')
    parser.add_argument('-e',
                        dest='environment',
                        choices=['prod', 'staging', 'dev'],
                        default='production',
                        help='Environment where to deploy')
    parser.add_argument('-n',
                        dest='nginx',
                        default='on',
                        choices=['on', 'off'],
                        help='Install Nginx reverse proxy')
    parser.add_argument('-v',
                        dest='verbose',
                        default='off',
                        choices=['on', 'off'],
                        help='Verbose mode')
    parser.add_argument('-d',
                        dest='debug',
                        default='off',
                        choices=['on', 'off'],
                        help='force restart and change debug mode')
    parser.add_argument('--database',
                        dest='database',
                        help='Default database')
    parser.add_argument('--test_database',
                        dest='test_database',
                        help='test database for QA')
    parser.add_argument('--defapp',
                        dest='defapp',
                        help='git path for default main application')
    parser.add_argument('--image',
                        dest='image',
                        default='Manifest',
                        help='odoo image, ovewrite the default manifest image')


def new_update_parser(sub):
    parser = sub.add_parser('update',
                            help='creates or updates an installation.')
    parser.add_argument('-r',
                        action='store_true',
                        help='Restart server')
    parser.add_argument('-q',
                        action='store_true',
                        help='Quick mode, do not pull repos and images')


def new_backup_parser(sub):
    parser = sub.add_parser('backup',
                            help='generates a backup in the backup_dir '
                                 'folder')
    parser.add_argument('-d',
                        dest='database',
                        help='Database to backup, if ommited the database in '
                             'config will be backed up')


def new_up_parser(sub):
    parser = sub.add_parser('up',
                            help='Start docker images')


def new_down_parser(sub):
    parser = sub.add_parser('down',
                            help='Stop docker images')


def new_restore_parser(sub):
    parser = sub.add_parser('restore',
                            help='restores a database from backup_dir')

    parser.add_argument('-r',
                        dest='database',
                        help='Database file to restore, if ommited, last '
                             'backup found in backup_dir will be restored')


def new_qa_parser(sub):
    parser = sub.add_parser('qa',
                            help='quality analisys')
    parser.add_argument('-d',
                        dest='test_database',
                        help='test database for qa, if ommited, the default'
                             'found in config will be used')


def parse():
    """ parsear los argumentos y completarlos con los datos almacenados en la
        configuracion devuelve un diccionario con los parametros
    """

    parser = argparse.ArgumentParser(description="""
==============================================================================
Odoo Environment {} - by jeo Software <jorge.obiols@gmail.com>
==============================================================================
""".format(__version__))

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(__version__))
    parser.add_argument('-H',
                        dest='help',
                        help='odoo server server help')

    subparser = parser.add_subparsers(help='commands', dest='command')
    new_config_parser(subparser)
    new_update_parser(subparser)
    new_up_parser(subparser)
    new_down_parser(subparser)
    new_backup_parser(subparser)
    new_restore_parser(subparser)
    new_qa_parser(subparser)

    # obtengo los comandos del runstring
    args = parser.parse_args()

    # le agrego los comandos almacenados
    data = merge_args(args, get_config())
    save_config(data)

    if args.command:
        if args.command == 'config':
            return command_config(data)

        if args.command == 'update':
            return command_update(data)

    if args.command:
        data['command'] = args.command
