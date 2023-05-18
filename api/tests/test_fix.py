import random
import shutil

import pytest
from config import settings
from storage import storage
from tests import DEFAULT_FILE

"""
Test case for fix file endpoint
@name file:fix_file
@router put /file/
@status_code 200
@response_model schemas.Msg
"""


class TestFixFile:
    @pytest.mark.usefixtures("create_file")
    async def test_fix_file_success(self):
        # random pick a block to corrupted
        block_id = random.randint(0, settings.NUM_DISKS - 1)
        path = storage.block_path[block_id]
        shutil.rmtree(path)

        # fix the block and check if the content is correct
        await storage.fix_block(block_id)
        content = await storage.retrieve_file(DEFAULT_FILE.name)
        assert content.decode() == DEFAULT_FILE.content
