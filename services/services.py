from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import email_validator
import passlib.hash as hash
from jwt import encode, decode
from datetime import datetime, timedelta

from database import database
from models import models
from schemas import user_schema, favorite_schema

JWT_SECRET = "edvorafullstackassessmentsecretjwtkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2Schema = OAuth2PasswordBearer("/api/users/login")

def create_database():
    return database.Base.metadata.create_all(bind=database.engine)

def get_database():
    db = database.SessionLocal()
    try:
        yield db
    except Exception as e:
        print("Unable to get db: ", e)
    finally:
        db.close()

async def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()

async def create_user(user: user_schema.UserCreate, db: Session):
    try:
        valid = email_validator.validate_email(email=user.email)
        email = valid.email
    except email_validator.EmailNotValidError:
        raise HTTPException(status_code=400, detail="Please enter a valid email")

    hashed_password = hash.bcrypt.hash(user.password)
    user_obj = models.User(first_name=user.first_name, 
                            last_name=user.last_name, 
                            email=email, 
                            hashed_password=hashed_password)

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def create_token(user: models.User):
    user_schema_obj = user_schema.User.from_orm(user)
    user_dict = user_schema_obj.dict()
    del user_dict["created_at"]
    to_encode = user_dict.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    token = encode(user_dict, JWT_SECRET, ALGORITHM)
    return dict(access_token=token, token_type="bearer")

async def authenticate_user(email: str, password: str, db: Session):
    user = await get_user_by_email(email=email, db=db)

    if not user:
        return False

    if not user.verify_password(password=password):
        return False

    return user


async def get_current_user(db: Session = Depends(get_database), token: str = Depends(oauth2Schema)):
    try:
        payload = decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user = db.query(models.User).get(payload["id"])
    except:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return user_schema.User.from_orm(user)

async def add_favorite_pokemon(user: user_schema.User, db: Session, favorite: favorite_schema.FavoriteCreate):
    favorite = models.Favorites(**favorite.dict(), owner_id=user.id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite_schema.Favorite.from_orm(favorite)


async def get_user_favorite_pokemons(user: user_schema.User, db: Session):
    favorites = db.query(models.Favorites).filter_by(owner_id=user.id)

    return list(map(favorite_schema.Favorite.from_orm, favorites))

async def remove_favorite_pokemon(user: user_schema.User, db: Session, favorite: favorite_schema.FavoriteRemove):
    poke = models.Favorites(**favorite.dict(), owner_id=user.id)
    data_to_delete = db.query(models.Favorites).filter_by(owner_id=user.id, pokemon_id=poke.pokemon_id).first()

    db.delete(data_to_delete)
    db.commit()

    favorites = db.query(models.Favorites).filter_by(owner_id=user.id)

    return list(map(favorite_schema.Favorite.from_orm, favorites))
