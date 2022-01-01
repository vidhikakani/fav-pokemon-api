from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from schemas import favorite_schema, user_schema
from services import services

router = APIRouter()


@router.post("/add-favorite-pokemon", response_model=favorite_schema.Favorite)
async def add_favorite_pokemon(favorite: favorite_schema.FavoriteCreate, 
                            user: user_schema.User = Depends(services.get_current_user),
                            db: Session = Depends(services.get_database)):
    return await services.add_favorite_pokemon(user=user, db=db, favorite=favorite)


@router.get("/get-favorite-pokemons", response_model=List[favorite_schema.Favorite])
async def get_user_favorite_pokemons(user: user_schema.User = Depends(services.get_current_user),
                                db: Session = Depends(services.get_database)):
    return await services.get_user_favorite_pokemons(user=user, db=db)

@router.post("/remove-favorite-pokemon", response_model=List[favorite_schema.Favorite])
async def get_user_favorite_pokemons(favorite: favorite_schema.FavoriteRemove,
                                user: user_schema.User = Depends(services.get_current_user),
                                db: Session = Depends(services.get_database)):
    return await services.remove_favorite_pokemon(user=user, db=db, favorite=favorite)