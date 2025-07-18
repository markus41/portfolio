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


class BaseTransport:
    """Mimic the minimal httpx BaseTransport interface used by Starlette."""

    async def handle_async_request(self, request):  # pragma: no cover - interface
        raise NotImplementedError


class MockTransport(BaseTransport):
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


class Client:
    """Synchronous wrapper used by FastAPI's TestClient."""

    def __init__(self, transport=None, base_url=""):
        self._async = AsyncClient(transport=transport, base_url=base_url)

    def get(self, path, params=None):
        import asyncio

        return asyncio.get_event_loop().run_until_complete(
            self._async.get(path, params=params)
        )

    def post(self, path, json=None):
        import asyncio

        return asyncio.get_event_loop().run_until_complete(
            self._async.post(path, json=json)
        )

    def close(self):
        pass


_client = type(
    "_client",
    (),
    {
        "CookieTypes": object,
        "UseClientDefault": object(),
        "USE_CLIENT_DEFAULT": object(),
    },
)

_types = type("_types", (), {"URLTypes": object})
