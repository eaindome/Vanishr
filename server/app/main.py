from fastapi import FastAPI
from app.api.routers import router

app = FastAPI(title="Incogni-Lite API")
app.include_router(router)
