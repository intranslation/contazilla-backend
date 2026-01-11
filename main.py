from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import engine, Base
from routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)


@app.get("/")
def health():
    return "ok"
