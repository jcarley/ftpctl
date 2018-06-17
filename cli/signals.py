from __future__ import absolute_import
from __future__ import unicode_literals

import signal

class ShutdownException(Exception):
    pass


class HangUpException(Exception):
    pass


def shutdown(signal, frame):
    raise ShutdownException()


def set_signal_handler(handler):
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)


def set_signal_handler_to_shutdown():
    set_signal_handler(shutdown)


def hang_up(signal, frame):
    raise HangUpException()


def set_signal_handler_to_hang_up():
    signal.signal(signal.SIGHUP, hang_up)


def ignore_sigpipe():
    # Restore default behavior for SIGPIPE instead of raising
    # an exception when encountered.
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

