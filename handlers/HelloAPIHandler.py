# -*- coding: utf-8 -*-

import logging
from tornado import web

logger = logging.getLogger(__name__)


class HelloAPIHandler(web.RequestHandler):

    def get(self):
        self.write('Hello !')
        return
