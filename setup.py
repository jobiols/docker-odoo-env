# -*- coding: utf-8 -*-

import setuptools
from __init__ import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="docker_odoo_env",
    version=__version__,
    author="jeo Software",
    author_email="jorge.obiols@gmail.com",
    description='A small tool to manage Dockerized Odoo',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jobiols/docker_odoo_env",
    entry_points={
        'console_scripts': ['oen=docker_odoo_env.command_line:main'],
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing :: Unit",
        "Topic :: System :: Software Distribution",
    ],
      keywords="odoo docker environment",
)
