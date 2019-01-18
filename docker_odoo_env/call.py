# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root
import subprocess


def call(command):
    # TODO sudo toma el password de un programa askpass, esto solo debe funcionar
    # en test habria que deshabiltarlo para uso normal.
    if 'sudo' in command:
        command = command.replace('sudo', '')
        command = 'SUDO_ASKPASS=/home/jobiols/git-repos/docker_odoo_env/docker_odoo_env/askpass.py sudo ' + command
    subprocess.call(command, shell=True)
