from pydantic import BaseModel, conint


class VoteBase(BaseModel):
    post_id: int
    dir: conint(le=1)
    
class VoteBody(VoteBase):
    pass

class VoteResponse(VoteBase):
    pass