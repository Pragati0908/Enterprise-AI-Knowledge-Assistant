from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import global_exception_handler

from app.middleware.request_logger import RequestLoggerMiddleware

from app.api.endpoints.health import router as health_router
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.upload import router as upload_router
from app.api.endpoints.documents import router as documents_router


app = FastAPI(
    title=settings.APP_NAME,
    description="Production Ready RAG Platform",
    version=settings.VERSION
)


# Register Middleware

app.add_middleware(RequestLoggerMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Register Global Exception Handler

app.add_exception_handler(
    Exception,
    global_exception_handler
)


@app.get("/")
def home():
    return {
        "message": "Enterprise AI Knowledge Assistant API",
        "status": "Running Successfully"
    }


@app.get("/settings")
def get_settings():
    return {
        "app_name": settings.APP_NAME,
        "version": settings.VERSION,
        "debug": settings.DEBUG,
        "host": settings.HOST,
        "port": settings.PORT,
        "log_level": settings.LOG_LEVEL
    }


@app.get("/error")
def test_error():
    raise Exception("Testing error handler")


# Register Routers

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(documents_router)