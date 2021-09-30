#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from tornado import web, options
from handlers import HelloAPIHandler, EchoAPIHandler, MainHandler

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# app's title
__title__ = 'Micro-Service Squeleton'

# get CLI options
options.define('port', default=8080, help='run on the given port', type=int)
options.define('logfile', default=None, help='file to write log, omit to output on stdout/err', type=str)
options.define('verbosity', default='INFO', help='log verbosity : CRITICAL, ERROR, WARNING, INFO, DEBUG', type=str)
options.parse_command_line(final=False)

# create the root logger
logging.basicConfig(filename=options.options.logfile, level=options.options.verbosity)

logger = logging.getLogger(__name__)


def main():
    settings = {
        'static_path': './static',
        'template_path': './templates',
    }
    application = web.Application([
            (r'/', MainHandler),
            (r'/api/hello/?', HelloAPIHandler),  # "/?" to allow a trailing "/" in the URL
            (r'/api/echo(.*)$', EchoAPIHandler),  # catch everything after "echo"
        ], **settings
    )
    logger.info(f'tornado web application will be listening on port : {options.options.port}')
    application.listen(port=options.options.port)


if __name__ == '__main__':
    main()
