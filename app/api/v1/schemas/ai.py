from pydantic import BaseModel


class AIProfileAnalyzeResponse(BaseModel):
    response: str
