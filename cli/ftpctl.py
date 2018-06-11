import socket
import click
import docker

from pathlib import Path
from cli.start import start
from cli.stop import stop
from cli.logging import info, error


@click.group()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.pass_context
def main(ctx, verbose):
    """
    This is an example script to learn Click.  Use this only as an example.
    Not meant for production use.

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
