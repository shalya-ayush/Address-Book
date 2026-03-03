from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.addresses import router as address_router

app = FastAPI(title=settings.PROJECT_NAME,
              description=settings.PROJECT_DESCRIPTION,
              version=settings.PROJECT_VERSION)

app.include_router(address_router, prefix=settings.API_V1_STR + "/addresses", tags=["addresses"])