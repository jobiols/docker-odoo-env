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

        # Actualizar instalacion
        msg.inf('Updating Server')
        subprocess.call('sudo ls', shell=True)

        p = subprocess.Popen(['sudo docker', '-v'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             shell=True)

        stdout = p.communicate()[0]

        subprocess.call('sudo apt-get update && sudo apt-get upgrade -y',
                        shell=True)
