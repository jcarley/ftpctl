import click
import docker
import sys

from . import signals
from .const import CONTAINER_NAME
from cli.logging import info, error

@click.command()
@click.option('--username', prompt='Your username', help="The username to remove")
@click.pass_context
def removeuser(ctx, username):

    cmd = "pure-pw userdel {0} -f /etc/pure-ftpd/passwd/pureftpd.passwd -m".format(username)

    create_exec_options = {
        "privileged": True,
    }

    client = docker.from_env()

    signals.set_signal_handler_to_shutdown()
    try:
        container = client.containers.get('ftpd_server')
        exit_code, output = container.exec_run(cmd, **create_exec_options)
    except signals.ShutdownException:
        error(ctx, "received shutdown exception: closing")

    sys.exit(exit_code)

