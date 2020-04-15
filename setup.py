# -*- coding: utf-8 -*-

import setuptools
from dov import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="docker-odoo-env",
    version=__version__,
    author='Jorge E. Obiols',
    author_email="jorge.obiols@gmail.com",
    description='A small tool to manage Dockerized Odoo',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jobiols/docker-odoo-env",
    python_requires='>3.0',
    entry_points={
        'console_scripts': [
            'oe=dov.click:click',
            'sd=dov.sd:main',
            ],
    },
    install_requires=['PyYAML', 'six', 'tornado', 'click'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Framework :: Odoo",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Testing :: Unit",
        "Topic :: System :: Software Distribution",
    ],
    keywords="odoo docker environment",
)
