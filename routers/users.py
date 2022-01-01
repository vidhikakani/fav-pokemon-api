from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas import user_schema
from services import services

router = APIRouter()

@router.post("/signup")
async def signup(user: user_schema.UserCreate,
                      db: Session = Depends(services.get_database)):
    db_user = await services.get_user_by_email(email=user.email, db=db)

    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user = await services.create_user(user=user, db=db)

    return await services.create_token(user=user)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                        db: Session = Depends(services.get_database)):
    # data = form_data.parse()
    # print(data.username)
    user = await services.authenticate_user(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return await services.create_token(user)


@router.get("/me", response_model=user_schema.User)
async def get_user(user: user_schema.User = Depends(services.get_current_user)):
    return user