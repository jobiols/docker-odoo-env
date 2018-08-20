# -*- coding: utf-8 -*-

import os
import json
import argparse
from version import VERSION
from messages import Msg

msg = Msg()

user_config_path = os.path.expanduser('~') + '/.config/oe/'
user_config_file = user_config_path + 'config.json'


def merge_args(args,data):
    return data


def command_config(data):
    msg.run('Saved options')
    print json.dumps(data, indent=4)


def command_update(args, data):
    if args.debug:
        data['debug'] = args.debug
    if args.client:
        data['client'] = args.client
    return data


def save_config(data):
    if not os.path.exists(user_config_path):
        os.makedirs(user_config_path)
    with open(user_config_file, 'w') as config:
        json.dump(data, config)


def get_config():
    if os.path.isfile(user_config_file):
        with open(user_config_file, 'r') as config:
            return json.load(config)
    else:
        return {}


def new_config_parser(sub):
    parser = sub.add_parser('config',
                            help='config current configuration')
    parser.add_argument('-c',
                        dest='cleanup',
                        help='Cleanup config data')


def new_update_parser(sub):
    parser = sub.add_parser('update',
                            help='creates or updates an installation')
    parser.add_argument('-d',
                        dest='debug',
                        choices=['on', 'off'],
                        help='Debug mode')
    parser.add_argument('-c',
                        dest='client',
                        help='Client code')


def new_backup_parser(sub):
    parser = sub.add_parser('backup',
                            help='generates a backup in the backup_dir '
                                 'folder')


def new_dependency_parser(sub):
    parser = sub.add_parser('dependency',
                            help='check and install dependencies')


def new_restore_parser(sub):
    parser = sub.add_parser('restore',
                            help='restores a database from backup_dir')


def parse():
    """ parsear los argumentos y completarlos con los datos almacenados en la
        configuracion devuelve un diccionario con los parametros
    """

    parser = argparse.ArgumentParser(description="""
==========================================================================
Odoo Environment Manager {} - by jeo Software <jorge.obiols@gmail.com>
==========================================================================
""".format(VERSION))

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(VERSION))
    parser.add_argument('-H',
                        dest='help',
                        help='odoo server server help')

    subparser = parser.add_subparsers(help='commands', dest='command')
    new_config_parser(subparser)
    new_update_parser(subparser)
    new_dependency_parser(subparser)
    new_backup_parser(subparser)
    new_restore_parser(subparser)

    # obtengo los comandos del runstring
    args = parser.parse_args()
    # le agrego los comandos almacenados
    data = merge_args(args, get_config())

    if args.command:
        if args.command == 'config':
            return command_config(data)

        if args.command == 'update':
            return command_update(args, data)

    save_config(data)

    if args.command:
        data['command'] = args.command
