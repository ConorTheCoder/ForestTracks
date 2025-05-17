from urllib import request, error
import json

class HTTPError(Exception):
    pass

class Response:
    def __init__(self, data, status):
        self._data = data
        self.status_code = status

    def json(self):
        return json.loads(self._data.decode())

    def raise_for_status(self):
        if 400 <= self.status_code:
            raise HTTPError(f'Status code: {self.status_code}')


def get(url):
    try:
        resp = request.urlopen(url)
        data = resp.read()
        status = resp.getcode()
        return Response(data, status)
    except error.HTTPError as e:
        raise HTTPError(str(e))
