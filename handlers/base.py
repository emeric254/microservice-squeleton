# -*- coding: utf-8 -*-

import json
import logging
import datetime
from tornado import web
from typing import Set

logger = logging.getLogger(__name__)


class BaseHandler(web.RequestHandler):
    allow_cors = True

    def data_received(self, _):
        """Override.

        :param _: chunk of data received
        """
        pass

    def set_default_headers(self):
        """Override.

        Prepare header to allow CORS
        """
        # allow hosts
        self.set_header('Access-Control-Allow-Origin', '*')
        # allow methods
        self.set_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PUT, PATCH, DELETE, OPTIONS')
        # allow requests headers
        self.set_header('Access-Control-Allow-Headers', 'Content-type, Authorization')
        # allow credentials (eg. foreign tokens)
        self.set_header('Access-Control-Allow-Credentials', 'true')
        # expose responses headers to web browser too
        self.set_header('Access-Control-Expose-Headers', 'Content-range')

    def prepare(self):
        """Override.

        Parse request body as JSON if possible.
        """
        self.json_args = {}
        content_type = self.request.headers.get('Content-Type', '')

        if content_type.startswith('application/json'):
            try:
                self.json_args = json.loads(self.request.body)
            except json.JSONDecodeError:
                raise web.HTTPError(status_code=400, log_message='Request body is not a valid json')

    def options(self, *_):
        """Override.

        Configure CORS
        """
        if self.allow_cors:
            # 204 (No content)
            self.set_status(204)
            return

        raise web.HTTPError(status_code=403, log_message='CORS not allowed')

    #
    # ------------------------------------------------------------------------------------------------------------------
    # argument parsing

    def parse_bool_argument(self, argument_name: str) -> bool:
        return self.get_query_argument(argument_name).lower() not in ('false', '0', 'no')

    def parse_str_argument(self, argument_name: str, allow_multiple: bool = False) -> str or Set[str]:
        if allow_multiple:
            return set(x for x in self.get_query_arguments(argument_name))
        return self.get_query_argument(argument_name)

    def parse_int_argument(self, argument_name: str, allow_multiple: bool = False) -> int or Set[int]:
        if allow_multiple:
            return set(int(x) for x in self.get_query_arguments(argument_name))
        return int(self.get_query_argument(argument_name))

    def parse_float_argument(self, argument_name: str, allow_multiple: bool = False) -> float or Set[float]:
        if allow_multiple:
            return set(float(x) for x in self.get_query_arguments(argument_name))
        return float(self.get_query_argument(argument_name))

    def parse_datetime_argument(self, argument_name: str, allow_multiple: bool = False) \
            -> datetime.datetime or Set[datetime.datetime]:
        if allow_multiple:
            return set(
                datetime.datetime.fromisoformat(x.replace('Z', ''))
                for x in self.get_query_arguments(argument_name)
            )
        return datetime.datetime.fromisoformat(self.get_query_argument(argument_name).replace('Z', ''))

    def parse_date_argument(self, argument_name: str, allow_multiple: bool = False) \
            -> datetime.date or Set[datetime.date]:
        if allow_multiple:
            return set(
                datetime.date.fromisoformat(x.replace('Z', ''))
                for x in self.get_query_arguments(argument_name)
            )
        return datetime.date.fromisoformat(self.get_query_argument(argument_name).replace('Z', ''))

    def parse_time_argument(self, argument_name: str, allow_multiple: bool = False) \
            -> datetime.time or Set[datetime.time]:
        if allow_multiple:
            return set(
                datetime.time.fromisoformat(x.replace('Z', ''))
                for x in self.get_query_arguments(argument_name)
            )
        return datetime.time.fromisoformat(self.get_query_argument(argument_name).replace('Z', ''))

    def parse_timedelta_argument(self, argument_name: str, allow_multiple: bool = False) \
            -> datetime.timedelta or Set[datetime.timedelta]:
        if allow_multiple:
            return set(
                datetime.timedelta(seconds=x)
                for x in self.parse_float_argument(argument_name, allow_multiple=True)
            )
        return datetime.timedelta(seconds=self.parse_float_argument(argument_name))
