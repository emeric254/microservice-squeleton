# -*- coding: utf-8 -*-

import logging
import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.process
import tornado.web

logger = logging.getLogger(__name__)


def start_http(app: tornado.web.Application, http_port: int = 80):
    """Create app instance(s) binding a port.

    :param app: the app to execute in server instances
    :param http_port: port to bind
    """
    http_socket = tornado.netutil.bind_sockets(http_port)  # HTTP socket
    try:  # try to create threads
        tornado.process.fork_processes(0)  # fork
    except KeyboardInterrupt:  # except KeyboardInterrupt to "properly" exit
        tornado.ioloop.IOLoop.current().stop()
    except AttributeError:  # OS without fork() support ...
        logger.warning('Can\' fork, continuing with only one (the main) thread ...')
        pass  # do nothing and continue without multi-threading
    logger.info('Start an HTTP request handler on port : ' + str(http_port))
    tornado.httpserver.HTTPServer(app).add_sockets(http_socket)  # bind http port
    try:  # try to stay forever alive to satisfy user's requests, except KeyboardInterrupt to "properly" exit
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()
