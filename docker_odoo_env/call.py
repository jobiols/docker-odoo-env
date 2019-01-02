# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root
import subprocess


def call(command):
    subprocess.call(command, shell=True)
