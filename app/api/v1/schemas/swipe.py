from pydantic import BaseModel


class SwipeRequest(BaseModel):
    liker_id: int
    liked_id: int
    decision: bool
    
class SwipeResponse(SwipeRequest):
    pass