import datetime as dt
import pydantic

class FavoriteBase(pydantic.BaseModel):
    pokemon_id: int


class FavoriteCreate(FavoriteBase):
    pass

class FavoriteRemove(FavoriteBase):
    pass


class Favorite(FavoriteBase):
    id: int
    owner_id: int
    created_at: dt.datetime

    class Config:
        orm_mode = True