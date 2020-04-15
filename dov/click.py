"""Hola."""

import click
import os

from odoo_env.odooenv import OdooEnv, OdooEnv_
from odoo_env.messages import Msg
from odoo_env.options import get_param
from odoo_env.__init__ import __version__
from odoo_env.config import OeConfig


CONTEXT_SETTINGS = dict(help_option_names=['-h'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-v', is_flag=True, help='verbose')
def cli(v):
    """Odoo Environment by jeo Software <jorge.obiols@gmail.com>."""

# RESTART -----------------------------------------------------------------


@click.command('restart')
def restart():
    """Restart Services."""
    click.echo('Restarting services')

# CONFIG ------------------------------------------------------------------


@cli.command('config')
def config():
    """Validate and view system configuration."""
    OdooEnv_()._config()

# IMAGES ------------------------------------------------------------------


@cli.command('images')
def images():
    """List images."""
    click.echo('listing images')

# PS ----------------------------------------------------------------------


@cli.command('ps')
@click.option('-a', is_flag=True, help="Show all containers")
def ps(a):
    """List containers."""
    if a:
        click.echo('List all running containers')
    else:
        click.echo('List running containers')

# GROUP -----------------------------------------------------------------------


@cli.command('pull')
def pull():
    """Pull service images."""
    click.echo('Pulling images...')

# VERSION ---------------------------------------------------------------------


@cli.command('version')
def version():
    """Show version information."""
    click.echo('oe version %s' % __version__)

# UP --------------------------------------------------------------------------


@cli.command("up")
@click.option('-c', help='client name')
@click.option('-d', help='database name')
@click.option('-e', type=click.Choice(['prod', 'debug']), help='environment')
def up(c, d, e):
    """Create and start containers."""

# PGADMIN ---------------------------------------------------------------------


@cli.command('pgadmin')
def pgadmin():
    """Start pgadmin."""
    click.echo('starting pgadmin')

# INSTALL----------------------------------------------------------------------


@cli.command('install')
def install():
    """Install Environment."""
    click.echo('installing...')

# HELP-------------------------------------------------------------------------


@cli.group('help')
def help():
    """Get help on a command."""


def _show_help(command):
    try:
        data_dir = os.path.join(os.path.dirname(__file__))
        with open(data_dir + '/doc/%s.hlp' % command, 'r') as f:
            help = f.read()
        click.echo_via_pager(help)
    except FileNotFoundError as e:
        click.echo(e)


@help.command('up')
def _help_up():
    _show_help('up')


@help.command('down')
def _help_down():
    _show_help('down')


@help.command('ps')
def _help_ps():
    _show_help('ps')


@help.command('backup')
def _help_backup():
    _show_help('backup')


@help.command('restore')
def _help_restore():
    _show_help('restore')


@help.command('config')
def _help_config():
    _show_help('config')

# DOWN ------------------------------------------------------------------------


@cli.command("down")
def down():
    """Stop and remove containers, networks, images, and volumes."""
    click.echo('System is going down...')

# DATABASE --------------------------------------------------------------------


@cli.group('db')
def db():
    """Database operations."""


@db.command('backup')
@click.option('-c', help='client name')
@click.option('-d', help='database name')
@click.option('-e', type=click.Choice(['prod', 'debug']), help='environment')
def _backup_database(c, d, e):
    """Backup current database to default location."""
    click.echo('Backing up database...')


@db.command('restore')
@click.option('-f', help='File to restore / latest file if ommited.')
@click.option('--prod', is_flag=True,
              help='Restore from production / local if ommited.')
@click.option('--no-deactivate', is_flag=True,
              help='Do not deactivate database.')
def _restore_database(f, prod, no_deactivate):
    """Restore backup from default location / production location."""
    click.echo('Restoring database from local...')


@db.command('list')
@click.option('--prod', is_flag=True,
              help='List from production / local if ommited.')
def _list_database(prod):
    """List backup files from default location / production location."""
    OdooEnv_()._list_database(prod=False)


if __name__ == "__main__":
    cli()
