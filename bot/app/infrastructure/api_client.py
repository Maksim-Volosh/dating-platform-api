from app.infrastructure.http_client import HTTPClient, http

JsonType = dict | list | None

class APIClient:
    def __init__(self, http: HTTPClient):
        self._http = http

    async def get(self, path: str):
        return await self._http.request("GET", path)

    async def post(self, path: str, json: JsonType = None, expected_status=201):
        return await self._http.request(
            "POST",
            path,
            json=json,
            expected_status=expected_status,
        )
        
    async def put(self, path: str, json: JsonType = None, expected_status=200):
        return await self._http.request(
            "PUT",
            path,
            json=json,
            expected_status=expected_status,
        )
        
    async def patch(self, path: str, json: JsonType = None, expected_status=200):
        return await self._http.request(
            "PATCH",
            path,
            json=json,
            expected_status=expected_status,
        )

api = APIClient(http)