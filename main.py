import fastapi
from fastapi.middleware.cors import CORSMiddleware

import routers
from services import services

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

services.create_database()

app.include_router(routers.router, prefix="/api", tags=['users'])