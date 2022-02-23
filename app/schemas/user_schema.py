from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
   

#::::::::::::::::::::[Body recived from frontend]::::::::::::::::
class CreateUserBody(UserBase):
    password: str
    
    
#::::::::::::::::::::[Response sent to backend]::::::::::::::::::
class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True