# -*- coding: utf-8 -*-

import os
import json
import argparse
from version import VERSION
from messages import Msg
msg = Msg()

user_config_path = os.path.expanduser('~') + '/.config/oe/'
user_config_file = user_config_path + 'config.json'


def command_show(data):
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


def parse():
    """ parsear los argumentos y completarlos con los datos almacenados en la
        configuracion devuelve un diccionario con los parametros
    """

    parser = argparse.ArgumentParser(description="""
==========================================================================
Odoo Environment Manager {} - by jeo Software <jorge.obiols@gmail.com>
==========================================================================
""".format(VERSION))

    sub = parser.add_subparsers(help='commands',
                                dest='command')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(VERSION))
    parser.add_argument('-H',
                        dest='help',
                        help='odoo server server help')

    show_p = sub.add_parser('show',
                            help='show current configuration')
    update_p = sub.add_parser('update',
                              help='creates or updates an installation')
    dependency_p = sub.add_parser('dependency',
                                  help='check and install dependencies')
    backup_p = sub.add_parser('backup',
                              help='generates a backup in the backup_dir '
                                   'folder')
    restore_p = sub.add_parser('restore',
                               help='restores a database from backup_dir')

    update_p.add_argument('-d',
                          dest='debug',
                          choices=['on', 'off'],
                          help='Debug mode')
    update_p.add_argument('-c',
                          dest='client',
                          help='Client code')

    args = parser.parse_args()
    data = get_config()

    if args.command:
        if args.command == 'show':
            return command_show(data)

        if args.command == 'update':
            return command_update(args, data)

    save_config(data)

    if args.command:
        data['command'] = args.command

    return data
