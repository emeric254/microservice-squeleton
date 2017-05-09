# -*- coding: utf-8 -*-

import logging
from tornado import web

logger = logging.getLogger(__name__)


class FakeAPIHandler(web.RequestHandler):

    def set_default_headers(self):  # to allow CORS
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):  # to allow CORS
        # no body
        self.set_status(204)
        self.finish()

    def get(self, path_request):
        if path_request == '' or path_request == '/':
            logger.info('user did not write anything')
            self.write('You do not provide anything to echo :(')
            return
        elif path_request.startswith('/'):
            path_request = path_request[1:]
            logger.info('user wrote : ' + path_request)
            self.write(path_request)
            return
        logger.error('Unknow error or the user send a really bad request : ' + path_request)
        self.send_error(status_code=500, reason='Server Internal Error')
        return
