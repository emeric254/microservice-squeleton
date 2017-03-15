# -*- coding: utf-8 -*-

import logging
from tornado import httpserver, ioloop, netutil, process, web

logger = logging.getLogger(__name__)


def start_http(app: web.Application, http_port: int = 80):
    """Create app instance(s) binding a port.

    :param app: the app to execute in server instances
    :param http_port: port to bind
    """
    http_socket = netutil.bind_sockets(http_port)  # HTTP socket
    try:  # try to create threads
        process.fork_processes(0)  # fork
    except KeyboardInterrupt:  # except KeyboardInterrupt to "properly" exit
        ioloop.IOLoop.current().stop()
    except AttributeError:  # OS without fork() support ...
        logger.warning('Can\' fork, continuing with only one (the main) thread ...')
        pass  # do nothing and continue without multi-threading
    try:  # try to stay forever alive to satisfy user's requests, except KeyboardInterrupt to "properly" exit
        logger.info('Start an HTTP request handler on port : ' + str(http_port))
        httpserver.HTTPServer(app).add_sockets(http_socket)  # bind http port
        ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        ioloop.IOLoop.current().stop()
