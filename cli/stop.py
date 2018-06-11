import click
import docker

from cli.logging import info

@click.command()
@click.pass_context
def stop(ctx):

    client = docker.from_env()
    try:
        info(ctx, "Shutting down ftpd_server.  This can take up to a minute.")
        container = client.containers.get('ftpd_server')
        container.stop()
    except docker.errors.NotFound:
        info(ctx, "Server not found to be running.")
    finally:
        info(ctx, "Done.")

