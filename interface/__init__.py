from fastapi import FastAPI
from contextlib import asynccontextmanager


from shared.database import engine, Base
from .controllers import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/v1/docs",  # Swagger UI
    openapi_url="/api/v1/openapi.json",  # OpenAPI schema JSON
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
)

app.include_router(auth_router, prefix="/api/v1")


@app.get("/api/v1")
def health():
    return "ok"
