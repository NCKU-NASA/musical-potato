import base64
from typing import BinaryIO

import pytest
import schemas
from httpx import Response
from tests import DEFAULT_FILE, RequestBody, ResponseBody, assert_request

"""
Test cases for create file endpoints
@name file:create_file
@router post /file/
@status_code 201
@response_model schemas.File
"""


class TestCreateFile:
    async def test_create_file_success(self, file: BinaryIO):
        req = RequestBody(
            url="file:create_file",
            body=None,
            files={"file": ("m3ow87.txt", file, "text/plain")},
        )
        resp = ResponseBody(
            status_code=201,
            body={
                **DEFAULT_FILE.dict(),
                **{"content": base64.b64encode(DEFAULT_FILE.content.encode()).decode()},
            },
        )
        await assert_request("post", req, resp)

    @pytest.mark.usefixtures("create_file")
    async def test_create_file_duplicate(self, file: BinaryIO):
        req = RequestBody(
            url="file:create_file",
            body=None,
            files={"file": ("m3ow87.txt", file, "text/plain")},
        )
        resp = ResponseBody(status_code=409, body={"detail": "File already exists"})
        await assert_request("post", req, resp)

    async def test_create_file_too_large(self, large_file: BinaryIO):
        req = RequestBody(
            url="file:create_file",
            body=None,
            files={"file": ("large_file.txt", large_file, "text/plain")},
        )
        resp = ResponseBody(status_code=413, body={"detail": "File too large"})
        await assert_request("post", req, resp)


"""
Test case for retrieve file endpoint
@name file:retrieve_file
@router get /file/
@status_code 200
@response_model str
"""


class TestRetrieveFile:
    def __assert_func(self, resp: Response, resp_body: ResponseBody):
        assert resp.status_code == resp_body.status_code
        assert resp.content.decode() == resp_body.body

    @pytest.mark.usefixtures("create_file")
    async def test_retrieve_file_success(self):
        req = RequestBody(
            url="file:retrieve_file", body=None, params={"filename": DEFAULT_FILE.name}
        )
        resp = ResponseBody(status_code=200, body=DEFAULT_FILE.content)
        await assert_request("get", req, resp, self.__assert_func)

    async def test_retrieve_file_none_exists(self):
        req = RequestBody(
            url="file:retrieve_file", body=None, params={"filename": "non-exists.txt"}
        )
        resp = ResponseBody(status_code=404, body={"detail": "File not found"})
        await assert_request("get", req, resp)


"""
Test case for update file endpoint
@name file:update_file
@router put /file/
@status_code 200
@response_model schemas.File
"""


class TestUpdateFile:
    EDITED_FILE: schemas.File = schemas.File(
        name="m3ow87.txt",
        size=29,
        checksum="ffa812690ae8afb4e6c651190a24b275",
        content="Let's M3ow M3ow M3ow All Day!",
        content_type="text/plain",
    )

    @pytest.mark.file_data(EDITED_FILE)
    @pytest.mark.usefixtures("create_file")
    async def test_update_file_success(self, file: BinaryIO):
        req = RequestBody(
            url="file:update_file",
            body=None,
            files={"file": ("m3ow87.txt", file, "text/plain")},
        )
        resp = ResponseBody(
            status_code=200,
            body={
                **self.EDITED_FILE.dict(),
                **{
                    "content": base64.b64encode(
                        self.EDITED_FILE.content.encode()
                    ).decode()
                },
            },
        )
        await assert_request("put", req, resp)

    async def test_update_file_none_exists(self, file: BinaryIO):
        req = RequestBody(
            url="file:update_file",
            body=None,
            files={"file": ("non-exists.txt", file, "text/plain")},
        )
        resp = ResponseBody(status_code=404, body={"detail": "File not found"})
        await assert_request("put", req, resp)

    @pytest.mark.usefixtures("create_file")
    async def test_update_file_too_large(self, large_file: BinaryIO):
        req = RequestBody(
            url="file:update_file",
            body=None,
            files={"file": ("m3ow87.txt", large_file, "text/plain")},
        )
        resp = ResponseBody(status_code=413, body={"detail": "File too large"})
        await assert_request("put", req, resp)


"""
Test case for delete file endpoint
@name file:delete_file
@router delete /file/
@status_code 200
@response_model schemas.File
"""


class TestDeleteFile:
    @pytest.mark.usefixtures("create_file")
    async def test_delete_file_success(self):
        req = RequestBody(
            url="file:delete_file", body=None, params={"filename": DEFAULT_FILE.name}
        )
        resp = ResponseBody(status_code=200, body={"detail": "File deleted"})
        await assert_request("delete", req, resp)

    async def test_delete_file_none_exists(self):
        req = RequestBody(
            url="file:delete_file", body=None, params={"filename": "non-exists.txt"}
        )
        resp = ResponseBody(status_code=404, body={"detail": "File not found"})
        await assert_request("delete", req, resp)
