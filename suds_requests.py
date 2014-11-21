import functools
import requests
import suds.transport as transport
import traceback
import io


__all__ = ['RequestsTransport']


class RequestsTransport(transport.Transport):
    def __init__(self, session=None):
        transport.Transport.__init__(self)
        self._session = session or requests.Session()

    def open(self, request):
        resp = self._session.get(request.url)
        return io.BytesIO(resp.content)

    def send(self, request):
        resp = self._session.post(
            request.url,
            data=request.message,
            headers=request.headers,
        )

        resp.raise_for_status()

        return transport.Reply(
            resp.status_code,
            resp.headers,
            resp.content,
        )
