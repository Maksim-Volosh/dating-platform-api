from typing import List
from pydantic import BaseModel


class PhotoURL(BaseModel):
    url: str
    
class PhotoResponse(BaseModel):
    user_id: int
    photos: List[PhotoURL]