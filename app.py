#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import tornado.web
import tornado.options
from handlers.FakeAPIHandler import FakeAPIHandler
from handlers.MainHandler import MainHandler
from tools import server

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# app's title
__title__ = 'Micro-Service Squeleton'

tornado.options.define('port', default=8080, help='run on the given port', type=int)
tornado.options.define('logfile', default=None, help='file to write log', type=str)
tornado.options.define('verbosity', default='INFO', help='log verbosity : CRITICAL, ERROR, WARNING, INFO, DEBUG',
                       type=str)
tornado.options.parse_command_line(final=False)
logging.basicConfig(filename=tornado.options.options.logfile, level=tornado.options.options.verbosity)
logger = logging.getLogger(__name__)


def main():
    settings = {
        'static_path': './static',
        'template_path': './templates',
    }
    logger.debug('app settings defined')
    application = tornado.web.Application([
            (r'/', MainHandler),  # index.html
            (r'/api(.*)$', FakeAPIHandler),
        ], **settings)
    logger.debug('tornado web application created')
    logger.info('tornado web application will be launched on port : ' + str(tornado.options.options.port))
    server.start_http(app=application, http_port=tornado.options.options.port)


if __name__ == '__main__':
    main()
