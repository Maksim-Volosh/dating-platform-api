from typing import List
from pydantic import BaseModel


class PhotoURL(BaseModel):
    url: str
    
class PhotoCreateResponse(BaseModel):
    user_id: int
    photos: List[PhotoURL]