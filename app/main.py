from fastapi import FastAPI
from app.routes.test_routes import router

app = FastAPI(title="Adaptive Diagnostic Engine")

app.include_router(router)
