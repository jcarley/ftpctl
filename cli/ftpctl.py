import socket
import click
import docker

from pathlib import Path
from cli.start import start
from cli.stop import stop
from cli.adduser import adduser
from cli.removeuser import removeuser
from cli.logging import info, error


@click.group()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.pass_context
def main(ctx, verbose):
    """
    ftpctl is a command line interface for the pure-ftpd docker container.  It controls starting
    and stopping the container, binding it to the correct IP address and setting up the volumes
    to store user credentials and uploads.

    Examples:

      ftpctl --help

      ftpctl --verbose start

      ftpctl stop

    """

    home = Path.home()
    root = home.joinpath('.ftpctl')
    users_uploads = root.joinpath('ftpusers')
    users_credentials = root.joinpath('pure-ftpd', 'passwd')

    ctx.obj['HOME'] = home
    ctx.obj['ROOT'] = root
    ctx.obj['USERS_UPLOADS'] = users_uploads
    ctx.obj['USERS_CREDENTIALS'] = users_credentials

    init(ctx)

    if verbose:
        ctx.obj['VERBOSE'] = True
        info(ctx, "Entering VERBOSE mode.")


def init(ctx):
    users_uploads = ctx.obj.get('USERS_UPLOADS')
    users_credentials = ctx.obj.get('USERS_CREDENTIALS')

    if not users_uploads.exists():
        info(ctx, "Initializing users upload directory at: {0}".format(users_uploads))
        users_uploads.mkdir(parents=True, exist_ok=True)

    if not users_credentials.exists():
        info(ctx, "Initializing users credentials directory at: {0}".format(users_credentials))
        users_credentials.mkdir(parents=True, exist_ok=True)



main.add_command(start)
main.add_command(stop)
main.add_command(adduser)
main.add_command(removeuser)

