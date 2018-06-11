import click

def log(ctx, prefix, msg):
    click.echo("{0}{1}".format(prefix, msg))


def info(ctx, msg):
    if ctx.obj.get('VERBOSE', False):
        log(ctx, "[INFO] ", msg)


def error(ctx, msg):
    if ctx.obj.get('VERBOSE', False):
        log(ctx, "[ERROR] ", msg)
