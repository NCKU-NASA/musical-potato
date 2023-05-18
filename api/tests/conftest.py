import shutil
from pathlib import Path
from typing import BinaryIO, Generator

import pytest
import schemas
from app import APP
from config import settings
from fastapi import UploadFile
from fastapi.testclient import TestClient
from storage import storage
from tests import DEFAULT_FILE


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(APP) as tc:
        yield tc


@pytest.fixture(scope="function")
def file(request) -> Generator:
    # get file from marker if exists
    file: schemas.File = DEFAULT_FILE
    marker = request.node.get_closest_marker("file_data")
    if marker:
        file = marker.args[0]

    # create a file in tmp use to upload
    path = Path("/tmp") / file.name
    path.unlink(missing_ok=True)
    path.write_text(file.content)

    # yield file
    with open(path, "rb") as fp:
        yield fp


@pytest.fixture(scope="function")
def large_file() -> Generator:
    # create a file in tmp use to upload
    path = Path("/tmp") / "large_file.txt"
    path.unlink(missing_ok=True)

    # write 100MB + 1 byte to file
    with open(path, "wb") as fp:
        fp.seek(settings.MAX_SIZE)
        fp.write(b"\x6d\x65\x6f\x77\x38\x37")

    # yield file
    with open(path, "rb") as fp:
        yield fp


@pytest.fixture(autouse=True)
def clean_env():
    for path in storage.block_path:
        for child in path.glob("*"):
            if child.is_file():
                child.unlink()
            else:
                shutil.rmtree(child)


@pytest.fixture()
async def create_file(file: BinaryIO) -> None:
    # create a file to be used for testing duplicate
    upload_file = UploadFile(
        filename="m3ow87.txt", file=file, content_type="text/plain"
    )
    await storage.create_file(upload_file)
