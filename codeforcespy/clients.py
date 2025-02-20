import httpx


class AsyncClient(httpx.AsyncClient):
    pass


class SyncClient(httpx.Client):
    pass
