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


class UpdateCommand(Command):

    def execute(self):

        # Si no estoy en desarrollo, intenta hacer un backup de la base de
        # datos activa, podria no haber base si es la primera instalacion.
        if self._config.args.get('environment') not in ['dev']:
            command = BackupCommand(self._config)
            command.execute()

        # Si no estoy en desarrollo verifica las dependencias en el servidor y
        # las instala o actualiza (apt-get update y docker)
        if self._config.args.get('environment') not in ['dev']:
            command = UpgradeCommand(self._config)
            command.execute()

        # Baja todas las imagenes docker (si estan activas)
        command = DockerDownCommand(self._config)
        command.execute()

        # hace pull de todos los repos y las imagenes
        command = PullCommand(self._config)
        command.execute()

        # crea, actualiza el odoo.conf, segun en que ambiente estemos
        command = OdooConfCommand(self._config)
        command.execute()

        # hace un update all dos veces (filtrando mensajes info)
        # instala o si esta instalada, actualiza la aplicacion por defecto
        command = UpdateAll(self._config)
        command.execute()

        # levanta todas las imagenes finales
        command = DockerUpCommand(self._config)
        command.execute()
