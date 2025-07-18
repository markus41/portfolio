class Response:
    def __init__(self, status_code=200, json=None, **kwargs):
        self.status_code = status_code
        self._json = json
        self.request = kwargs.get("request")
        
    def json(self):
        return self._json


class URL:
    def __init__(self, url: str):
        self.scheme = "http"
        self.netloc = b"testserver"
        self.path = url
        self.raw_path = url.encode()
        self.query = b""


class Request:
    def __init__(self, method, url, json=None, params=None):
        self.method = method
        self.url = URL(url)
        self.headers = {}
        self._json = json
        self._params = params
        self._content = b""

    def json(self):
        return self._json

    def read(self) -> bytes:
        return self._content


class BaseTransport:
    pass


class MockTransport(BaseTransport):
    def __init__(self, handler):
        self.handler = handler

    async def handle_async_request(self, request):
        return await self.handler(request)

    def handle_request(self, request):
        return self.handler(request)


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


class Client:
    def __init__(self, *, transport=None, base_url="", app=None, headers=None, follow_redirects=True, cookies=None):
        self.transport = transport or MockTransport(lambda req: Response())
        self.base_url = base_url
        self.app = app

    def request(self, method, path, **kwargs):
        req = Request(
            method,
            path,
            json=kwargs.get("json"),
            params=kwargs.get("params"),
        )
        return self.transport.handle_request(req)

    def get(self, path, params=None, **kwargs):
        req = Request("GET", path, params=params)
        return self.transport.handle_request(req)

    def post(self, path, json=None, **kwargs):
        req = Request("POST", path, json=json)
        return self.transport.handle_request(req)

    def close(self):
        pass


class _ClientModule:
    class UseClientDefault:
        pass

    CookieTypes = object
    TimeoutTypes = object
    USE_CLIENT_DEFAULT = UseClientDefault()


_client = _ClientModule()


class _TypesModule:
    URLTypes = object
    QueryParamTypes = object
    RequestContent = object
    RequestFiles = object
    HeaderTypes = object
    CookieTypes = object
    AuthTypes = object


_types = _TypesModule()
