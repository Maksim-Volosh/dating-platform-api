from pydantic import BaseModel


class LikeCreateRequest(BaseModel):
    liker_id: int

class LikeCreateResponse(BaseModel):
    count: int
    
class LikeNextResponse(BaseModel):
    liker_id: int
    