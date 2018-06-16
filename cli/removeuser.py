import click
import docker
import sys

@click.command()
@click.option('--username', prompt='Your username', help="The username to remove")
@click.pass_context
def removeuser(ctx, username):

    CONTAINER_NAME = 'ftpd_server'

    cmd = "pure-pw userdel {0} -f /etc/pure-ftpd/passwd/pureftpd.passwd -m".format(username)

    create_exec_options = {
        "privileged": True,
    }

    client = docker.from_env()
    container = client.containers.get('ftpd_server')
    exit_code, output = container.exec_run(cmd, **create_exec_options)
    sys.exit(exit_code)

