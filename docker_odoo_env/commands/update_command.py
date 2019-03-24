# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.commands.command import Command
from docker_odoo_env.commands.backup_command import BackupCommand
from docker_odoo_env.commands.upgrade_command import UpgradeCommand
from docker_odoo_env.commands.docker_down_command import DockerDownCommand
from docker_odoo_env.commands.pull_command import PullCommand
from docker_odoo_env.commands.odoo_conf_command import OdooConfCommand
from docker_odoo_env.commands.docker_up_command import DockerUpCommand
from docker_odoo_env.commands.update_all import UpdateAll
from docker_odoo_env.commands.directory_hierarchy_command import DirectoryHierarchyCommand
from docker_odoo_env.messages import msg
from docker_odoo_env.config import conf_


class UpdateCommand(Command):

    def execute(self):
        if not conf_.args.get('client'):
            msg.err('Must define a client')
        if not conf_.args.get('defapp'):
            msg.err('Must define a default application')

        if conf_.args.get('doc'):
            self.show_doc()

        # Testear si esta creada la estructura de directorios y crearla si no
        # existe
        command = DirectoryHierarchyCommand()
        command.execute()

        # Si no estoy en desarrollo, intenta hacer un backup de la base de
        # datos activa, podria no haber base si es la primera instalacion.
        if conf_.args.get('environment') not in ['dev']:
            command = BackupCommand()
            command.execute()

        # Baja todas las imagenes docker (si estan activas)
        command = DockerDownCommand()
        command.execute()

        # Si no estoy en desarrollo verifica las dependencias en el servidor y
        # las instala o actualiza (apt-get update y docker)
        if conf_.args.get('environment') not in ['dev']:
            command = UpgradeCommand()
            command.execute()

        # hace clone o pull de todos los repos y las imagenes
        command = PullCommand()
        command.execute()

        # crea, actualiza el odoo.conf, segun en que ambiente estemos
        command = OdooConfCommand()
        command.execute()

        # hace un update all dos veces (filtrando mensajes info)
        # instala o si esta instalada, actualiza la aplicacion por defecto
        command = UpdateAll()
        command.execute()

        # levanta todas las imagenes finales
        command = DockerUpCommand()
        command.execute()
