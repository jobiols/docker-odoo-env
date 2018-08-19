# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="docker_odoo_env",
    version="0.0.1",
    author="jeo Software",
    author_email="jorge.obiols@gmail.com",
    description='A small tool to manage Dockerized Odoo',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jobiols/docker_odoo_env",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)