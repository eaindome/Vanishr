from fastapi import FastAPI
from app.api.routers import router

app = FastAPI(title="Vanishr API")
app.include_router(router)
