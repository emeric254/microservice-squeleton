# -*- coding: utf-8 -*-

import json
import logging
from handlers.base import BaseHandler

logger = logging.getLogger(__name__)


class EchoAPIHandler(BaseHandler):
    def get(self, echoed_part):
        if echoed_part == '' or echoed_part == '/':
            logger.info('user did not write anything')
            return
        if echoed_part.startswith('/'):
            echoed_part = echoed_part[1:]
        logger.info(f'user wrote : {echoed_part}')
        self.write(echoed_part)

    def post(self, _):
        if self.json_args:
            # you could do some stuff on the given JSON before returning it
            logger.info('user give use a json to echo pretty printed')
            self.write(json.dumps(self.json_args, indent=2))
            return
        # echo the raw body from the post request
        logger.info('user will receive body copy from the request one')
        self.write(self.request.body)
