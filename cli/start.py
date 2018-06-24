import sys
import socket
import click
import docker

from docker.errors import NotFound

from . import progress_stream
from .const import CONTAINER_NAME, IMAGE_NAME
from .progress_stream import stream_output
from .progress_stream import StreamOutputError
from .logging import info, error

@click.command()
@click.option('--host', default='', help="The IP address to bind the ftp service to.")
@click.pass_context
def start(ctx, host):

    REMOVE_ON_SHUTDOWN = True
    RUN_DETACHED = True

    if len(host) > 0:
        ip = host
    else:
        ip = socket.gethostbyname(socket.gethostname())

    if ip == '127.0.0.1':
        error(ctx, "Can't bind ftp service to loopback.")
        error(ctx, "Please provide the ip addrss to bind to using the --host option.")
        exit()

    if not exists(ctx):
        pull(ctx)

    info(ctx, "Starting ftp-server at host {0}".format(ip))

    users_uploads = ctx.obj.get('USERS_UPLOADS')
    users_credentials = ctx.obj.get('USERS_CREDENTIALS')

    client = docker.from_env()
    container = client.containers.run(IMAGE_NAME,
            detach=RUN_DETACHED,
            auto_remove=REMOVE_ON_SHUTDOWN,
            name=CONTAINER_NAME,
            ports={'21/tcp':21},
            environment=["PUBLICHOST={0}".format(ip)],
            volumes={users_uploads: {'bind': '/home/ftpusers/', 'mode': 'rw'},
                    users_credentials: {'bind': '/etc/pure-ftpd/passwd', 'mode': 'rw'}})

def exists(ctx):
    repo, tag, separator = parse_repository_tag(IMAGE_NAME)
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    images = client.images(repo, quiet=True)
    return len(images) > 0


def pull(ctx, ignore_pull_failures=False):

    repo, tag, separator = parse_repository_tag(IMAGE_NAME)
    kwargs = {
        'tag': tag or 'latest',
        'stream': True,
    }

    info(ctx, 'Pulling %s (%s%s%s)...' % ('pure-ftp', repo, separator, tag))

    try:
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        output = client.pull(repo, **kwargs)
        return progress_stream.get_digest_from_pull(
            stream_output(output, sys.stdout))
    except (StreamOutputError, NotFound) as e:
        if not ignore_pull_failures:
            raise
        else:
            error(ctx, six.text_type(e))


def parse_repository_tag(repo_path):
    """Splits image identification into base image path, tag/digest
    and it's separator.

    Example:

    >>> parse_repository_tag('user/repo@sha256:digest')
    ('user/repo', 'sha256:digest', '@')
    >>> parse_repository_tag('user/repo:v1')
    ('user/repo', 'v1', ':')
    """
    tag_separator = ":"
    digest_separator = "@"

    if digest_separator in repo_path:
        repo, tag = repo_path.rsplit(digest_separator, 1)
        return repo, tag, digest_separator

    repo, tag = repo_path, ""
    if tag_separator in repo_path:
        repo, tag = repo_path.rsplit(tag_separator, 1)
        if "/" in tag:
            repo, tag = repo_path, ""

    return repo, tag, tag_separator
