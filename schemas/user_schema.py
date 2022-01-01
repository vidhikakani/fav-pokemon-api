import datetime as dt
import pydantic

class UserBase(pydantic.BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    created_at: dt.datetime

    class Config:
        orm_mode = True