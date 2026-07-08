from fastapi import FastAPI

from app.api.endpoints.health import router as health_router
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.upload import router as upload_router
from app.api.endpoints.documents import router as documents_router

app = FastAPI(
    title="Enterprise AI Knowledge Assistant",
    description="Production Ready RAG Platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Enterprise AI Knowledge Assistant API",
        "status": "Running Successfully"
    }

# Register Routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(documents_router)