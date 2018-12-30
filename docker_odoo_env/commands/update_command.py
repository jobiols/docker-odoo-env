# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from command import Command
from backup_command import BackupCommand
from upgrade_command import UpgradeCommand
from docker_down_command import DockerDownCommand
from pull_command import PullCommand


class UpdateCommand(Command):

    def execute(self):

        # Si no estoy en desarrollo, intenta hacer un backup de la base de
        # datos activa, podria no haber base si es la primera instalacion.
        if self._config.args['environment'] not in ['dev']:
            backup = BackupCommand
            backup.execute()

        # Si no estoy en desarrollo verifica las dependencias en el servidor y
        # las instala o actualiza (apt-get update y docker)
        if self._config.args['environment'] not in ['dev']:
            upgrade = UpgradeCommand
            upgrade.execute()

        # Baja todas las imagenes docker (si estan activas)
        docker_down = DockerDownCommand
        docker_down.execute()

        # hace pull de todos los repos y las imagenes
        pull = PullCommand
        pull.execute()

        # Levanta image postgres y aeroo (a veces aeroo no es requerido)
        docker_up_env

