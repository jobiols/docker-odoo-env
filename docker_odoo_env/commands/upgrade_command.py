# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.commands.command import Command
import subprocess
from docker_odoo_env.messages import Msg

msg = Msg()


class UpgradeCommand(Command):
    def execute(self):
        if self._config.args.get('doc'):
            self.show_doc()

        msg.inf('Updating Server')

        """
        from subprocess import Popen, PIPE
        import getpass
        # Actualizar instalacion

        command = 'docker -v'.split()
        p = Popen(['sudo', '-S'] + command,
                  stdin=PIPE, stdout=PIPE, stderr=PIPE,
                  universal_newlines=True)
        passw = getpass.getpass('')
        sudo_prompt = p.communicate(passw+'\n')

        print(sudo_prompt[0])

        """
        command = 'sudo docker -v'
        subprocess.call(command, shell=True)
