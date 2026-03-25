import httpx
from fastmcp.server.dependencies import get_http_request

class MCPForwardAuth(httpx.Auth):
    def auth_flow(self, request):
        try:
            req = get_http_request()
            auth = req.headers.get("Authorization")
            if auth:
                request.headers["Authorization"] = auth
        except Exception:
            pass
        yield request