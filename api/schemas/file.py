from pydantic import BaseModel


# File Schema
class File(BaseModel):
    name: str
    size: int
    checksum: str
    content: str
    content_type: str
