# -*- coding: utf-8 -*-

import logging
from handlers.base import BaseHandler

logger = logging.getLogger(__name__)


class MainHandler(BaseHandler):
    """Handle '/' endpoint (root server endpoint).
    """

    def get(self):
        """Handle GET requests. Serve the index web page.
        """
        logger.debug('rendering index.html file')
        self.render('index.html')
