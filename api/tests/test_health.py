from tests import RequestBody, ResponseBody, assert_request


async def test_get_health_success() -> None:
    req = RequestBody(url="health:get_health", body=None)
    resp = ResponseBody(status_code=200, body={"detail": "Service healthy"})
    await assert_request("get", req, resp)
