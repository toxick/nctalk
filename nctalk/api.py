"""Base API interface."""

import xmltodict
import json

from nextcloud import NextCloud
from urllib.parse import urlencode

from nctalk.exceptions import (
    NextCloudTalkException,
    NextCloudTalkBadRequest,
    NextCloudTalkForbidden,
    NextCloudTalkNotFound,
    NextCloudTalkConflict,
    NextCloudTalkPreconditionFailed,
    NextCloudTalkUnauthorized)


class NextCloudTalkAPI(object):
    """Base class for all API objects."""

    def __init__(self, client: NextCloud, api_endpoint: str):
        self.client = client
        self.endpoint = self.client.url + api_endpoint

    def query(
            self,
            data: dict = {},
            sub: str = '',
            method: str = 'GET',
            url: str = '',
            include_headers: list = []):
        """Submit query to almighty endpoint."""
        if method == 'GET':
            url_data = urlencode(data)
            request = self.client.session.request(
                url=f'{url}{sub}?{url_data}' if url else f'{self.endpoint}{sub}?{url_data}',
                method=method)
        else:
            request = self.client.session.request(
                url=f'{url}{sub}' if url else f'{self.endpoint}{sub}',
                method=method,
                data=data)

        if request.ok:
            # Convert OrderedDict from xmltodict.parse to regular dict.
            request_data = json.loads(json.dumps(xmltodict.parse(request.content)))
            try:
                ret = request_data['ocs']['data']
            except KeyError:
                raise NextCloudTalkException('Unable to parse response: ' + request_data)
            for header in include_headers:
                ret.setdefault('request_headers', {})\
                   .setdefault(header, request.headers.get(header, None))
        else:
            failure_data = xmltodict.parse(request.content)['ocs']['meta']
            exception_string = '[{statuscode}] {status}: {message}'.format(**failure_data)
            match failure_data['statuscode']:  # type: ignore
                case '400':
                    raise NextCloudTalkBadRequest(exception_string)
                case '401':
                    raise NextCloudTalkUnauthorized(exception_string)
                case '403':
                    raise NextCloudTalkForbidden(exception_string)
                case '404':
                    raise NextCloudTalkNotFound(exception_string)
                case '409':
                    raise NextCloudTalkConflict(exception_string)
                case '412':
                    raise NextCloudTalkPreconditionFailed(exception_string)
                case _:
                    raise NextCloudTalkException(exception_string)

        return ret
