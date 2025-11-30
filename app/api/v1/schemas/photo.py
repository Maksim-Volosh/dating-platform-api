from typing import List

from pydantic import BaseModel


class PhotoFileId(BaseModel):
    file_id: str
    
class PhotoResponse(BaseModel):
    user_id: int
    photos: List[PhotoFileId]