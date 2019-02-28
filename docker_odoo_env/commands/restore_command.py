# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.commands.command import Command
from docker_odoo_env.call import call


class RestoreCommand(Command):

    def restore(self, database_file):
        """ restaura un archivo del backup
        """
        client = self._config.args.get('client')
        command = 'sudo docker run --rm -i'
        command += '--link pg-{}:db '.format(client)
        command += '-v /odoo_ar/odoo-11.0/{}/backup_dir/:/backup '.format(client)
        command += '--env NEW_DBNAME={}_prod '.format(client)
        command += '--env DEACTIVATE=True '
        command += 'jobiols/dbtools'
        call(command)

    def remote_restore(self, remote_database_file):
        pass

    def execute(self):
        if self._config.args.get('doc'):
            self.show_doc()

        database_file = self._config.args.get('database_file')
        if database_file:
            self.restore(database_file)

        remote_database_file = self._config.args.get('remote_database_file')
        if remote_database_file:
            self.remote_restore(remote_database_file)
