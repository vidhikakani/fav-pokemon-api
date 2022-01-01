import fastapi
from fastapi.middleware.cors import CORSMiddleware

import routers

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

app.include_router(routers.router, prefix="/api", tags=['users'])