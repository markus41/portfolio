class Response:
    def __init__(self, status_code=200, json=None):
        self.status_code = status_code
        self._json = json

    def json(self):
        return self._json


class Request:
    def __init__(self, method, url, json=None, params=None):
        self.method = method
        self.url = type('URL', (), {'path': url})()
        self._json = json
        self._params = params

    def json(self):
        return self._json


class MockTransport:
    def __init__(self, handler):
        self.handler = handler

    async def handle_async_request(self, request):
        return await self.handler(request)


class AsyncClient:
    def __init__(self, transport=None, base_url=""):
        self.transport = transport or MockTransport(lambda req: Response())
        self.base_url = base_url

    async def post(self, path, json=None):
        req = Request("POST", path, json=json)
        return await self.transport.handle_async_request(req)

    async def get(self, path, params=None):
        req = Request("GET", path, params=params)
        return await self.transport.handle_async_request(req)

    async def aclose(self):
        pass

    def close(self):
        pass


# Compat with httpx.BaseTransport used by Starlette's test client
class BaseTransport:
    pass

# Starlette also expects a synchronous httpx.Client. Reuse AsyncClient for tests.
Client = AsyncClient


class _client:
    CookieTypes = dict
    UseClientDefault = object
    USE_CLIENT_DEFAULT = object


class _types:
    URLTypes = str
    AuthTypes = object
    TimeoutTypes = object
