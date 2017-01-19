# -*- coding: utf-8 -*-

import logging
import tornado.web

logger = logging.getLogger(__name__)


class MainHandler(tornado.web.RequestHandler):
    """Handle '/' endpoint (root server endpoint).
    """

    def get(self):
        """Handle GET requests. Serve the index web page.
        """
        logger.debug('render index.html file')
        self.render('index.html')
        return
