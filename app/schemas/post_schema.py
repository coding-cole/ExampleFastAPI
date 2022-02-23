from datetime import datetime
from pydantic import BaseModel

from .user_schema import UserResponse

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
    
#::::::::::::::::::::[Body recived from frontend]:::::::::::::::
class CreatePostBody(PostBase):
    pass


#::::::::::::::::::::[Response sent to frontend]::::::::::::::::
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    class Config:
        orm_mode = True
        
class MainPostResponse(BaseModel):
    Post: PostResponse
    votes: int
    class Config:
        orm_mode = True