from fastapi import FastAPI
from contextlib import asynccontextmanager


from shared.database import engine, Base
from .controllers import auth_router


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
