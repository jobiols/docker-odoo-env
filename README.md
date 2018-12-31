# Docker Odoo Environment

[![Build Status](https://travis-ci.org/jobiols/docker_odoo_env.svg?branch=master)](https://travis-ci.org/jobiols/docker_odoo_env)
[![codecov](https://codecov.io/gh/jobiols/docker_odoo_env/branch/master/graph/badge.svg)](https://codecov.io/gh/jobiols/docker_odoo_env)
[![CodeFactor](https://www.codefactor.io/repository/github/jobiols/docker_odoo_env/badge)](https://www.codefactor.io/repository/github/jobiols/docker_odoo_env)

This is a small tool to manage dockerized odoo environments develop
staging and production.
Still in development, this is not a release.

# Installation

To install with pip, run: `pip install docker-odoo-env`

# Usage

    usage: oe [-h] [--version] [-H HELP]
              {config,update,up,down,backup,restore,qa} ...
    
    ==============================================================================
    Odoo Environment 0.0.a10 - by jeo Software <jorge.obiols@gmail.com>
    ==============================================================================
    
    positional arguments:
      {config,update,up,down,backup,restore,qa}
                            commands
        config              config current configuration
        update              creates or updates an installation.
        up                  Start docker images
        down                Stop docker images
        backup              generates a backup in the backup_dir folder
        restore             restores a database from backup_dir
        qa                  quality analisys
    
    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -H HELP               odoo server server help
