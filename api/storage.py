import base64
import hashlib
import sys
from pathlib import Path
from typing import List

import schemas
from config import settings
from fastapi import UploadFile
from loguru import logger


class Storage:
    def __init__(self, is_test: bool):
        self.block_path: List[Path] = [
            Path("/tmp") / f"{settings.FOLDER_PREFIX}-{i}-test"
            if is_test
            else Path(settings.UPLOAD_PATH) / f"{settings.FOLDER_PREFIX}-{i}"
            for i in range(settings.NUM_DISKS)
        ]
        self.__create_block()

    def __create_block(self):
        for path in self.block_path:
            logger.warning(f"Creating folder: {path}")
            path.mkdir(parents=True, exist_ok=True)

    async def file_integrity(self, filename: str) -> bool:
        """TODO: check if file integrity is valid
        file integrated must satisfy following conditions:
            1. all data blocks must exist
            2. size of all data blocks must be equal
            3. parity block must exist
            4. parity verify must success

        if one of the above conditions is not satisfied
        the file does not exist
        and the file is considered to be damaged
        so we need to delete the file
        """
        return True

    async def create_file(self, file: UploadFile) -> schemas.File:
        # TODO: create file with data block and parity block and return it's schema

        content = "お前はもう死んでいる!!!"
        return schemas.File(
            name="m3ow.txt",
            size=123,
            checksum=hashlib.md5(content.encode()).hexdigest(),
            content=base64.b64decode(content.encode()),
            content_type="text/plain",
        )

    async def retrieve_file(self, filename: str) -> bytes:
        # TODO: retrieve the binary data of file

        return b"".join("m3ow".encode() for _ in range(100))

    async def update_file(self, file: UploadFile) -> schemas.File:
        # TODO: update file's data block and parity block and return it's schema

        content = "何?!"
        return schemas.File(
            name="m3ow.txt",
            size=123,
            checksum=hashlib.md5(content.encode()).hexdigest(),
            content=base64.b64decode(content.encode()),
            content_type="text/plain",
        )

    async def delete_file(self, filename: str) -> None:
        # TODO: delete file's data block and parity block
        pass

    async def fix_block(self, block_id: int) -> None:
        # TODO: fix the broke block by using rest of block
        pass


storage: Storage = Storage(is_test="pytest" in sys.modules)
