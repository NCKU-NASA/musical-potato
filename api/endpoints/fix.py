import schemas
from fastapi import APIRouter, status
from schemas import Msg
from storage import storage

router = APIRouter()


@router.post(
    "/{block_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Msg,
    name="fix:fix_block",
)
async def fix_block(block_id: int) -> schemas.File:
    await storage.fix_block(block_id)
    return Msg(detail="Block fixed")
