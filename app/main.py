from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.models import address
from app.api.v1.addresses import router as address_router
from app.db.database import SessionLocal, engine, Base
from app.core.logging import setup_logging

setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME,
              description=settings.PROJECT_DESCRIPTION,
              version=settings.PROJECT_VERSION)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

app.include_router(address_router, prefix=settings.API_V1_STR + "/addresses", tags=["addresses"])