# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.commands.command import Command
from docker_odoo_env.call import call
from docker_odoo_env.messages import msg


class RestoreCommand(Command):
    def restore(self, database_file):
        """ restaura un archivo del backup
        """
        client = self._config.args.get('client')
        if not client:
            msg.err('No client is configured in config')
        ver = self._config.args.get('ver')
        if not ver:
            msg.err('No Odoo version in config. '
                    'Did you install the default app?')

        filename = self._config.args.get('filename')
        command = 'sudo docker run --rm -i'
        command += '--link pg-{}:db '.format(client)
        command += '-v /odoo_ar/odoo-{}/{}/backup_dir/:/backup '.format(ver,
                                                                        client)
        if filename:
            command += '--env FILENAME={} '.format(filename)
        command += '--env NEW_DBNAME={}_prod '.format(client)
        command += '--env DEACTIVATE=True '
        command += 'jobiols/dbtools'
        call(command)

    def remote_restore(self, remote_database_file):
        pass

    def execute(self):
        if self._config.args.get('doc'):
            self.show_doc()

        # si ponen -r database_file tomo el le paso el nombre
        database_file = self._config.args.get('database_file')
        if database_file:
            self.restore(database_file)
            exit()

        # si ponen -R host database_file le paso los dos parametros (lista)
        remote_database_file = self._config.args.get('remote_database_file')
        if remote_database_file:
            self.remote_restore(remote_database_file)
            exit()

        # si no pone nada le paso false y restaura el mas nuevo
        self.restore(False)
        exit()
