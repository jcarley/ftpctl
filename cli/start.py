import socket
import click
import docker

from cli.logging import info, error

@click.command()
@click.option('--host', default='', help="The IP address to bind the ftp service to.")
@click.pass_context
def start(ctx, host):

    if len(host) > 0:
        ip = host
    else:
        ip = socket.gethostbyname(socket.gethostname())

    if ip == '127.0.0.1':
        error(ctx, "Can't bind ftp service to loopback.")
        error(ctx, "Please provide the ip addrss to bind to using the --host option.")
        exit()

    info(ctx, "Starting ftp-server at host {0}".format(ip))

    users_uploads = ctx.obj.get('USERS_UPLOADS')
    users_credentials = ctx.obj.get('USERS_CREDENTIALS')

    client = docker.from_env()
    container = client.containers.run('stilliard/pure-ftpd:stretch-latest',
            detach=True,
            auto_remove=True,
            name='ftpd_server',
            ports={'21/tcp':21},
            environment=["PUBLICHOST={0}".format(ip)],
            volumes={users_uploads: {'bind': '/home/ftpusers/', 'mode': 'rw'},
                    users_credentials: {'bind': '/etc/pure-ftpd/passwd', 'mode': 'rw'}})