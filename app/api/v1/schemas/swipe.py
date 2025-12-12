from pydantic import BaseModel


class SwipeRequest(BaseModel):
    liker_id: int
    liked_id: int
    decision: bool
    
class SwipeResponse(BaseModel):
    user1_id: int
    user1_decision: bool | None
    user2_id: int
    user2_decision: bool | None