# -*- coding: utf-8 -*-

import logging
from handlers.base import BaseHandler

logger = logging.getLogger(__name__)


class HelloAPIHandler(BaseHandler):

    def get(self):
        self.write('Hello !')
        return
