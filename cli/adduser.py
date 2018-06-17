import click
import docker
import sys

from . import signals
from .const import CONTAINER_NAME

from dockerpty.pty import PseudoTerminal, RunOperation, ExecOperation
from cli.logging import info, error

@click.command()
@click.option('--username', prompt='Your username', help="The username to add")
@click.pass_context
def adduser(ctx, username):

    cmd = "pure-pw useradd {0} -f /etc/pure-ftpd/passwd/pureftpd.passwd -m -u ftpuser -d /home/ftpusers/{0}".format(username)

    create_exec_options = {
        "privileged": True,
        "tty": True,
        "stdin": True,
    }

    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    exec_id = client.exec_create(CONTAINER_NAME, cmd, **create_exec_options)

    signals.set_signal_handler_to_shutdown()
    try:
        operation = ExecOperation(
            client,
            exec_id,
            interactive=True,
        )
        pty = PseudoTerminal(client, operation)
        pty.start()
    except signals.ShutdownException:
        error(ctx, "received shutdown exception: closing")

    exit_code = client.exec_inspect(exec_id).get("ExitCode")
    sys.exit(exit_code)


